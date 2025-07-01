import cv2
import numpy as np


def load_and_preprocess_image(image_path: str) -> tuple:
    image = cv2.imread(image_path)
    blurred = cv2.medianBlur(image, 3)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    return image, gray


def detect_edges(gray_image: np.ndarray) -> np.ndarray:
    return cv2.Canny(gray_image, 500, 650, apertureSize=5)


def detect_tray_bounds(edges: np.ndarray) -> tuple:
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90, minLineLength=50, maxLineGap=5)
    x_vals = [line[0][0] for line in lines]
    y_vals = [line[0][1] for line in lines]
    return min(x_vals), max(x_vals), min(y_vals), max(y_vals)


def draw_tray_rectangle(image: np.ndarray, bounds: tuple) -> None:
    min_x, max_x, min_y, max_y = bounds
    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (230, 230, 230), 3)


def detect_coins(gray_image: np.ndarray) -> np.ndarray:
    circles = cv2.HoughCircles(
        gray_image,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=10,
        param1=100,
        param2=35,
        minRadius=20,
        maxRadius=40
    )
    return np.uint16(np.around(circles)) if circles is not None else np.array([])


def classify_and_draw_coins(image: np.ndarray, coins: np.ndarray, bounds: tuple) -> tuple:
    min_x, max_x, min_y, max_y = bounds
    coins_inside = {'large': 0, 'small': 0}
    coins_outside = {'large': 0, 'small': 0}

    total_area_large = 0
    total_area_small = 0

    for coin in coins[0]:
        cx, cy, r = coin
        area = np.pi * r**2
        is_inside = min_x < cx < max_x and min_y < cy < max_y
        is_large = r > 31

        color_large = (200, 100, 255)
        color_small = (180, 220, 255)
        center_color = (40, 40, 40)

        if is_inside:
            if is_large:
                coins_inside['large'] += 1
                total_area_large += area
                color = color_large
            else:
                coins_inside['small'] += 1
                total_area_small += area
                color = color_small
            cv2.circle(image, (cx, cy), 3, center_color, 4)
        else:
            if is_large:
                coins_outside['large'] += 1
                total_area_large += area
                color = color_large
            else:
                coins_outside['small'] += 1
                total_area_small += area
                color = color_small

        cv2.circle(image, (cx, cy), r, color, 2)

    return coins_inside, coins_outside, total_area_large, total_area_small


def calculate_total(inside: dict, outside: dict) -> tuple:
    inside_val = inside['large'] * 5 + inside['small'] * 0.05
    outside_val = outside['large'] * 5 + outside['small'] * 0.05
    total = round(inside_val + outside_val, 2)
    return inside_val, outside_val, total


def print_results(inside: dict, outside: dict, totals: tuple, tray_area: float, large_coin_area: float) -> None:
    inside_val, outside_val, total = totals
    print(f"5 zł coins inside tray: {inside['large']}")
    print(f"5 zł coins outside tray: {outside['large']}")
    print(f"0.05 zł coins inside tray: {inside['small']}")
    print(f"0.05 zł coins outside tray: {outside['small']}")
    print(f"Total inside tray: {inside_val} zł")
    print(f"Total outside tray: {outside_val} zł")
    print(f"Total value: {total} zł\n")

    print(f"Tray area: {tray_area} px²")
    print(f"Single 5 zł coin area (example): {large_coin_area:.2f} px²")
    percent = (large_coin_area / tray_area) * 100
    print(f"5 zł coin is {percent:.4f}% the size of the tray.")


def main():
    image_path = 'pliki/tray7.jpg'

    image, gray = load_and_preprocess_image(image_path)
    edges = detect_edges(gray)
    bounds = detect_tray_bounds(edges)
    draw_tray_rectangle(image, bounds)

    coins = detect_coins(gray)
    min_x, max_x, min_y, max_y = bounds
    tray_area = (max_x - min_x) * (max_y - min_y)

    if coins.size > 0:
        inside, outside, area_large, area_small = classify_and_draw_coins(image, coins, bounds)
        totals = calculate_total(inside, outside)
        avg_large_coin_area = area_large / max(inside['large'] + outside['large'], 1)
        print_results(inside, outside, totals, tray_area, avg_large_coin_area)
        print(f"Total area of 5 zł coins: {area_large:.2f} px²")
        print(f"Total area of 0.05 zł coins: {area_small:.2f} px²")
    else:
        print("No coins detected.")

    cv2.imshow('Detected Coins', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
