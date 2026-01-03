def binary_search_upper_bound(arr, target):
    """
    arr – відсортований список дробових чисел (по зростанню).
    target – значення, для якого шукаємо верхню межу.
    Повертає (iterations, upper_bound), де
    upper_bound – найменший елемент із arr, що >= target,
    або None, якщо такого немає.
    """
    left, right = 0, len(arr) - 1
    upper_bound = None
    iterations = 0

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] >= target:
            upper_bound = arr[mid]
            right = mid - 1
        else:
            left = mid + 1

    return iterations, upper_bound


if __name__ == "__main__":
    data = [0.5, 1.2, 3.3, 4.4, 5.5]

    print(binary_search_upper_bound(data, 3.0))  # Наприклад: (3, 3.3)
    print(binary_search_upper_bound(data, 3.3))  # (кілька ітерацій, 3.3)
    print(binary_search_upper_bound(data, 6.0))  # (кілька ітерацій, None)