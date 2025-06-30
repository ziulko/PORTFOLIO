import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
import shap
import json
import os
import joblib
import sys

class DataOptimizer:
    def __init__(self, df, target_col, save_path='optimized_versions', balance_strategy='downsample'):
        self.original_df = self.clean_data(df.copy())
        self.target_col = target_col
        self.save_path = save_path
        self.balance_strategy = balance_strategy
        os.makedirs(save_path, exist_ok=True)
        self.iteration = 0
        self.best_versions = []
        self.models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced' if balance_strategy == 'class_weight' else None),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced' if balance_strategy == 'class_weight' else None),
            'DecisionTree': DecisionTreeClassifier(random_state=42, class_weight='balanced' if balance_strategy == 'class_weight' else None)
        }

    def clean_data(self, df):
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].median(), inplace=True)
            elif df[col].dtype == 'object':
                df[col] = df[col].astype(str)
                df[col].replace(['', 'nan', 'None', 'NaN'], np.nan, inplace=True)
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'unknown', inplace=True)
        return df

    def detect_data_types(self):
        numeric = self.original_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical = self.original_df.select_dtypes(include=['object', 'category']).columns.tolist()
        if self.target_col in numeric:
            numeric.remove(self.target_col)
        if self.target_col in categorical:
            categorical.remove(self.target_col)
        return numeric, categorical

    def preprocess(self, df, numeric, categorical):
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric),
                ('cat', categorical_transformer, categorical)])

        return preprocessor

    def balance_data(self, X, y):
        if self.balance_strategy == 'downsample':
            df_combined = pd.concat([X, y], axis=1)
            target_name = y.name
            majority_class = df_combined[target_name].value_counts().idxmax()
            minority_class = df_combined[target_name].value_counts().idxmin()

            df_majority = df_combined[df_combined[target_name] == majority_class]
            df_minority = df_combined[df_combined[target_name] == minority_class]

            df_majority_downsampled = resample(df_majority,
                                               replace=False,
                                               n_samples=len(df_minority),
                                               random_state=42)

            df_balanced = pd.concat([df_majority_downsampled, df_minority])
            df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

            return df_balanced.drop(columns=[target_name]), df_balanced[target_name]

        elif self.balance_strategy == 'upsample':
            df_combined = pd.concat([X, y], axis=1)
            target_name = y.name
            majority_class = df_combined[target_name].value_counts().idxmax()
            minority_class = df_combined[target_name].value_counts().idxmin()

            df_majority = df_combined[df_combined[target_name] == majority_class]
            df_minority = df_combined[df_combined[target_name] == minority_class]

            df_minority_upsampled = resample(df_minority,
                                             replace=True,
                                             n_samples=len(df_majority),
                                             random_state=42)

            df_balanced = pd.concat([df_majority, df_minority_upsampled])
            df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

            return df_balanced.drop(columns=[target_name]), df_balanced[target_name]

        elif self.balance_strategy == 'smote':
            sm = SMOTE(random_state=42)
            X_res, y_res = sm.fit_resample(X, y)
            return X_res, y_res

        else:
            return X, y

    def evaluate_and_store(self, df_version, X, y):
        X_bal, y_bal = self.balance_data(pd.DataFrame(X.toarray() if hasattr(X, 'toarray') else X), y.reset_index(drop=True))
        X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.2, random_state=42)

        best_score = 0
        best_model_name = None
        best_metrics = {}

        for name, model in self.models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            f1 = f1_score(y_test, preds, average='weighted')
            precision = precision_score(y_test, preds, average='weighted', zero_division=0)
            recall = recall_score(y_test, preds, average='weighted', zero_division=0)

            if f1 > best_score:
                best_score = f1
                best_model_name = name
                best_metrics = {
                    "f1_score": f1,
                    "precision": precision,
                    "recall": recall
                }

        version_path = os.path.join(self.save_path, f'version_{self.iteration}.pkl')
        joblib.dump(df_version, version_path)
        self.best_versions.append((best_score, version_path, best_model_name, best_metrics))
        self.best_versions = sorted(self.best_versions, key=lambda x: x[0], reverse=True)[:10]

        with open(os.path.join(self.save_path, 'metrics.json'), 'w') as f:
            json.dump([
                {"score": s, "path": p, "model": m, "metrics": mt}
                for s, p, m, mt in self.best_versions
            ], f, indent=4)

    def optimize(self):
        numeric, categorical = self.detect_data_types()
        X = self.original_df.drop(columns=[self.target_col])
        y = self.original_df[self.target_col]

        for i in range(3):
            print(f"--- Iteration {i+1} ---")
            self.iteration = i+1
            df_variant = self.original_df.copy()

            if i == 1:
                low_corr_features = self.low_correlation_features(df_variant, y)
                df_variant.drop(columns=low_corr_features, inplace=True, errors='ignore')

            if i == 2:
                df_variant = self.feature_engineering(df_variant)

            numeric, categorical = self.detect_data_types()
            preprocessor = self.preprocess(df_variant, numeric, categorical)
            X_processed = preprocessor.fit_transform(df_variant.drop(columns=[self.target_col]))
            self.evaluate_and_store(df_variant, X_processed, y)

    def low_correlation_features(self, df, y):
        corr = df.corrwith(y).abs()
        return corr[corr < 0.05].index.tolist()

    def feature_engineering(self, df):
        for col in df.select_dtypes(include=['int64', 'float64']).columns:
            df[f'{col}_log'] = np.log1p(df[col].abs())
        return df

    def generate_report(self):
        report = []
        for score, path, model, metrics in self.best_versions:
            report.append({"score": score, "dataset": path, "model": model, "metrics": metrics})
        with open(os.path.join(self.save_path, 'final_report.json'), 'w') as f:
            json.dump(report, f, indent=4)

if __name__ == '__main__':
    print("Witamy w Data Optimizerze!")
    file_path = input("Podaj ścieżkę do pliku CSV: ").strip()

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Błąd przy wczytywaniu pliku: {e}")
        sys.exit(1)

    print("\nPierwsze 3 wiersze danych:\n")
    print(df.head(3).to_string(index=False))

    print("\nKolumny w zbiorze danych:")
    for i, col in enumerate(df.columns):
        print(f"[{i}] {col}")

    try:
        idx = int(input("\nPodaj numer kolumny, która jest etykietą (targetem): "))
        target_col = df.columns[idx]
    except (IndexError, ValueError):
        print("Nieprawidłowy wybór kolumny.")
        sys.exit(1)

    strategy = input("Wybierz strategię balansowania (downsample / upsample / smote / class_weight): ").strip()
    if strategy not in ['downsample', 'upsample', 'smote', 'class_weight']:
        print("Nieprawidłowa strategia balansowania. Używam domyślnej: 'downsample'.")
        strategy = 'downsample'

    optimizer = DataOptimizer(df, target_col=target_col, balance_strategy=strategy)
    optimizer.optimize()
    optimizer.generate_report()
    print("\nProces optymalizacji zakończony. Wyniki zapisane w katalogu 'optimized_versions'.")
