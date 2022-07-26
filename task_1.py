# Поиск первого индекса нуля алгоритмом бинарного поиска
def task(array: str):
    left_side = 0
    right_side = len(array)
    mid = (right_side - left_side) // 2

    while right_side - left_side > 1:
        # Ищем по левой половине, если в середине ноль
        if array[mid] == "0":
            right_side = mid
        # Иначе по правой
        else:
            left_side = mid
        mid = left_side + (right_side + 1 - left_side) // 2
        # Если в середине ноль, а перед нулем единица - это искомый индекс, заканчиваем программу без полного
        # прохода цикла
        if array[mid-1] == "1" and array[mid] == "0":
            return mid

    # Сюда приходим, если преждевременного не пришли
    # Возвращаем из двух оставшихся индексов указывающий на ноль
    return left_side if array[left_side] == "0" else right_side


if __name__ == "__main__":
    array_to_check = input("Введите последовательность 1 и 0:\n")
    print(task(array_to_check))