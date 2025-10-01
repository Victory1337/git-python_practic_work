import math
import sys

def calculate_factorial(n):
    """
    Вычисляет факториал числа n с оптимизацией для больших чисел.
    
    Args:
        n (int): Положительное целое число
    
    Returns:
        int: Факториал числа n
    """
    # Используем math.factorial для оптимизации работы с большими числами
    return math.factorial(n)

def main():
    """
    Основная функция программы с обработкой ошибок ввода.
    """
    print("=== Программа для вычисления факториала ===")
    
    try:
        # Запрашиваем ввод от пользователя
        user_input = input("Введите положительное целое число: ")
        
        # Пытаемся преобразовать ввод в целое число
        number = int(user_input)
        
        # Проверяем, что число положительное
        if number < 0:
            print("Ошибка: Факториал определен только для неотрицательных чисел!")
            return
        
        # Вычисляем факториал
        result = calculate_factorial(number)
        
        # Выводим результат
        print(f"Факториал числа {number} равен: {result}")
        
        # Дополнительная информация для больших чисел
        if number > 10:
            print(f"Количество цифр в результате: {len(str(result))}")
            
    except ValueError:
        # Обработка случая, когда введены нечисловые данные
        print("Ошибка: Введите корректное целое число!")
    except OverflowError:
        # Обработка переполнения (хотя math.factorial обрабатывает большие числа хорошо)
        print("Ошибка: Число слишком большое для вычисления!")
    except KeyboardInterrupt:
        # Обработка прерывания программы пользователем
        print("\nПрограмма прервана пользователем")
        sys.exit(0)
    except Exception as e:
        # Общая обработка других возможных ошибок
        print(f"Произошла непредвиденная ошибка: {e}")

# Дополнительная функция для тестирования (DevOps подход)
def test_factorial():
    """
    Функция для тестирования корректности работы программы.
    """
    test_cases = [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800)
    ]
    
    print("\n=== Тестирование функции ===")
    for input_num, expected in test_cases:
        result = calculate_factorial(input_num)
        status = "✓" if result == expected else "✗"
        print(f"{status} factorial({input_num}) = {result} (ожидалось: {expected})")

if __name__ == "__main__":
    main()
    
    # Предлагаем пользователю запустить тесты
    choice = input("\nЗапустить тесты? (y/n): ").lower()
    if choice == 'y':
        test_factorial()