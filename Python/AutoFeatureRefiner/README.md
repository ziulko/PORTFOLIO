# Data Optimizer

## Project Description

**Data Optimizer** is an experimental data preprocessing pipeline designed to automatically clean, transform, balance, and evaluate datasets for machine learning tasks. Its goal is to streamline the feature selection and optimization process by analyzing data quality, applying statistical transformations, balancing class distributions, and testing multiple models in multiple iterations.

The tool is especially useful for prototyping ML workflows and exploring different preprocessing strategies without writing boilerplate code.

>⚠ **Note**: This project is in an early, non-final state. Some parts of the logic (e.g., feature ranking, iterative learning, explainability) are still under active development and may not behave optimally across all datasets. Expect instability or incomplete features.

---

## Current Features

- Automatic cleaning of numeric and text columns (including type correction and NaN handling)
- Feature correlation filtering
- Logarithmic feature transformation
- Multi-model evaluation (RandomForest, GradientBoosting, LogisticRegression, DecisionTree)
- F1, precision, and recall scoring
- Top 10 optimized dataset versions saved with metrics
- Balance strategies:
  - Downsampling
  - Upsampling
  - SMOTE
  - `class_weight='balanced'`
- Command-line interface for interactive dataset selection
- JSON report generation of all iterations and model performance

---

## Planned Features

- SHAP explainability and visualizations
- Auto-selection of best balance strategy
- HTML/PDF report generation
- Support for multiclass/multilabel targets
- GUI version with Streamlit or Gradio
- Integration with AutoML backends

---

## Technologies Used

- Python
- scikit-learn
- imbalanced-learn (SMOTE)
- pandas / NumPy
- joblib / JSON
- CLI with `input()` for now

---

## Development Notes

- No persistent database (uses local file storage)
- Report files (`metrics.json`, `final_report.json`) saved in `optimized_versions/`
- Meant for offline experimentation
- Needs improvement for very large or unbalanced datasets

---

## Feedback Welcome

If you have ideas for improving **Data Optimizer**, feel free to reach out! Suggestions for handling imbalanced data, new feature engineering ideas, or model explainability features are especially appreciated.
