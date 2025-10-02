# number_guessing_game.py
import random
import json
import datetime
import os

class NumberGuessingGame:
    """
    Класс для игры 'Угадай число'
    """
    
    def __init__(self, min_number=1, max_number=100, max_attempts=7):
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.target_number = 0
        self.attempts = 0
        self.used_numbers = []
        self.game_active = False
        self.stats_file = "game_statistics.json"
        self.load_statistics()
    
    def generate_number(self):
        """Генерация случайного числа"""
        self.target_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        self.used_numbers = []
        self.game_active = True
    
    def show_instructions(self):
        """Показать инструкцию к игре"""
        print("\n" + "="*50)
        print("🎯 ИГРА 'УГАДАЙ ЧИСЛО'")
        print("="*50)
        print(f"Я загадал число от {self.min_number} до {self.max_number}")
        print(f"У вас есть {self.max_attempts} попыток, чтобы угадать его!")
        print("\nПосле каждой попытки я подскажу:")
        print("  🔼 'Слишком маленькое' - если ваше число меньше")
        print("  🔽 'Слишком большое' - если ваше число больше")
        print("  🎉 'Поздравляю!' - если вы угадали!")
        print("\nКоманды:")
        print("  'help' - показать инструкцию")
        print("  'stats' - показать статистику")
        print("  'restart' - начать новую игру")
        print("  'quit' - выйти из игры")
        print("="*50 + "\n")
    
    def validate_input(self, user_input):
        """Валидация пользовательского ввода"""
        try:
            # Проверка специальных команд
            if user_input.lower() in ['quit', 'exit', 'q']:
                return 'QUIT'
            elif user_input.lower() in ['help', 'h']:
                return 'HELP'
            elif user_input.lower() in ['stats', 'statistics']:
                return 'STATS'
            elif user_input.lower() in ['restart', 'new', 'again']:
                return 'RESTART'
            
            # Преобразование в число
            guess = int(user_input)
            
            # Проверка диапазона
            if not (self.min_number <= guess <= self.max_number):
                return 'ERROR', f"❌ Число должно быть от {self.min_number} до {self.max_number}!"
            
            # Проверка на повторение
            if guess in self.used_numbers:
                return 'ERROR', "⚠️ Вы уже вводили это число! Попробуйте другое."
            
            return 'SUCCESS', guess
            
        except ValueError:
            return 'ERROR', "❌ Пожалуйста, введите целое число!"
    
    def get_user_guess(self):
        """Получить и проверить ввод пользователя"""
        while True:
            try:
                user_input = input(f"🎲 Попытка {self.attempts + 1}/{self.max_attempts}. Введите число: ")
                
                result = self.validate_input(user_input)
                
                if result == 'QUIT':
                    return 'QUIT'
                elif result == 'HELP':
                    self.show_instructions()
                    continue
                elif result == 'STATS':
                    self.show_statistics()
                    continue
                elif result == 'RESTART':
                    return 'RESTART'
                elif result[0] == 'ERROR':
                    print(result[1])
                    continue
                elif result[0] == 'SUCCESS':
                    self.attempts += 1
                    self.used_numbers.append(result[1])
                    return result[1]
                    
            except KeyboardInterrupt:
                print("\n\nИгра прервана пользователем")
                return 'QUIT'
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                continue
    
    def check_guess(self, guess):
        """Проверить предположение пользователя"""
        if guess == self.target_number:
            print(f"🎉 Поздравляю! Вы угадали число {self.target_number} за {self.attempts} попыток!")
            self.update_statistics(win=True)
            return 'WIN'
        elif guess < self.target_number:
            print("🔽 Слишком маленькое! Попробуйте число побольше")
        else:
            print("🔼 Слишком большое! Попробуйте число поменьше")
        
        # Дополнительные подсказки после нескольких попыток
        if self.attempts >= 3:
            self.provide_hint(guess)
        
        return 'CONTINUE'
    
    def provide_hint(self, guess):
        """Предоставить дополнительную подсказку"""
        difference = abs(guess - self.target_number)
        range_size = self.max_number - self.min_number
        
        if difference <= range_size * 0.1:  # В пределах 10% от диапазона
            print("   💡 Очень близко! Почти угадали!")
        elif difference <= range_size * 0.25:  # В пределах 25% от диапазона
            print("   💡 Достаточно близко! Продолжайте в том же духе!")
        elif self.attempts == self.max_attempts - 1:  # Последняя попытка
            if self.target_number % 2 == 0:
                print("   💡 Подсказка: число четное!")
            else:
                print("   💡 Подсказка: число нечетное!")
    
    def show_progress(self):
        """Показать прогресс игры"""
        remaining = self.max_attempts - self.attempts
        progress_bar = "█" * self.attempts + "░" * remaining
        print(f"Прогресс: [{progress_bar}] {self.attempts}/{self.max_attempts} попыток")
        print(f"Использованные числа: {sorted(self.used_numbers)}")
    
    def load_statistics(self):
        """Загрузить статистику из файла"""
        self.statistics = {
            'games_played': 0,
            'games_won': 0,
            'total_attempts': 0,
            'best_score': float('inf'),
            'win_streak': 0,
            'current_streak': 0,
            'history': []
        }
        
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded_stats = json.load(f)
                    self.statistics.update(loaded_stats)
        except Exception as e:
            print(f"⚠️ Не удалось загрузить статистику: {e}")
    
    def save_statistics(self):
        """Сохранить статистику в файл"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.statistics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Не удалось сохранить статистику: {e}")
    
    def update_statistics(self, win):
        """Обновить статистику"""
        self.statistics['games_played'] += 1
        
        if win:
            self.statistics['games_won'] += 1
            self.statistics['total_attempts'] += self.attempts
            self.statistics['current_streak'] += 1
            self.statistics['win_streak'] = max(self.statistics['win_streak'], self.statistics['current_streak'])
            
            if self.attempts < self.statistics['best_score']:
                self.statistics['best_score'] = self.attempts
            
            # Добавить в историю
            game_record = {
                'date': datetime.datetime.now().isoformat(),
                'target': self.target_number,
                'attempts': self.attempts,
                'result': 'win',
                'used_numbers': self.used_numbers
            }
            self.statistics['history'].append(game_record)
        else:
            self.statistics['current_streak'] = 0
            
            game_record = {
                'date': datetime.datetime.now().isoformat(),
                'target': self.target_number,
                'attempts': self.attempts,
                'result': 'lose',
                'used_numbers': self.used_numbers
            }
            self.statistics['history'].append(game_record)
        
        # Ограничить историю последними 50 играми
        if len(self.statistics['history']) > 50:
            self.statistics['history'] = self.statistics['history'][-50:]
        
        self.save_statistics()
    
    def show_statistics(self):
        """Показать статистику"""
        print("\n" + "="*40)
        print("📊 СТАТИСТИКА ИГРЫ")
        print("="*40)
        
        if self.statistics['games_played'] == 0:
            print("Статистика пока недоступна. Сыграйте хотя бы одну игру!")
            return
        
        win_rate = (self.statistics['games_won'] / self.statistics['games_played']) * 100
        
        print(f"Всего сыграно игр: {self.statistics['games_played']}")
        print(f"Побед: {self.statistics['games_won']} ({win_rate:.1f}%)")
        print(f"Лучший результат: {self.statistics['best_score']} попыток")
        
        if self.statistics['games_won'] > 0:
            avg_attempts = self.statistics['total_attempts'] / self.statistics['games_won']
            print(f"Среднее количество попыток: {avg_attempts:.1f}")
        
        print(f"Текущая серия побед: {self.statistics['current_streak']}")
        print(f"Лучшая серия побед: {self.statistics['win_streak']}")
        print("="*40)
    
    def play_round(self):
        """Играть один раунд"""
        self.generate_number()
        print(f"\n🎯 Новый раунд! Я загадал число от {self.min_number} до {self.max_number}")
        
        while self.game_active and self.attempts < self.max_attempts:
            self.show_progress()
            
            guess = self.get_user_guess()
            
            if guess == 'QUIT':
                self.game_active = False
                return 'QUIT'
            elif guess == 'RESTART':
                return 'RESTART'
            
            result = self.check_guess(guess)
            
            if result == 'WIN':
                self.game_active = False
                break
            
            if self.attempts >= self.max_attempts:
                print(f"\n💔 К сожалению, вы исчерпали все попытки!")
                print(f"💡 Загаданное число было: {self.target_number}")
                self.update_statistics(win=False)
                break
        
        return 'CONTINUE'
    
    def ask_play_again(self):
        """Спросить, хочет ли пользователь играть снова"""
        while True:
            try:
                choice = input("\nХотите сыграть еще раз? (y/n): ").lower().strip()
                
                if choice in ['y', 'yes', 'да', 'д']:
                    return True
                elif choice in ['n', 'no', 'нет', 'н']:
                    return False
                else:
                    print("Пожалуйста, введите 'y' (да) или 'n' (нет)")
            except KeyboardInterrupt:
                return False
            except Exception:
                return False
    
    def change_difficulty(self):
        """Изменить уровень сложности"""
        print("\n" + "="*30)
        print("🎚️ ВЫБОР СЛОЖНОСТИ")
        print("="*30)
        print("1. Легкий (1-50, 10 попыток)")
        print("2. Средний (1-100, 7 попыток)")
        print("3. Сложный (1-200, 5 попыток)")
        print("4. Эксперт (1-500, 3 попытки)")
        print("5. Настроить вручную")
        
        while True:
            try:
                choice = input("\nВыберите уровень сложности (1-5): ").strip()
                
                if choice == '1':
                    self.min_number, self.max_number, self.max_attempts = 1, 50, 10
                    break
                elif choice == '2':
                    self.min_number, self.max_number, self.max_attempts = 1, 100, 7
                    break
                elif choice == '3':
                    self.min_number, self.max_number, self.max_attempts = 1, 200, 5
                    break
                elif choice == '4':
                    self.min_number, self.max_number, self.max_attempts = 1, 500, 3
                    break
                elif choice == '5':
                    try:
                        min_num = int(input("Минимальное число: "))
                        max_num = int(input("Максимальное число: "))
                        attempts = int(input("Количество попыток: "))
                        
                        if min_num >= max_num:
                            print("Минимальное число должно быть меньше максимального!")
                            continue
                        if attempts <= 0:
                            print("Количество попыток должно быть положительным!")
                            continue
                        
                        self.min_number, self.max_number, self.max_attempts = min_num, max_num, attempts
                        break
                    except ValueError:
                        print("Пожалуйста, вводите целые числа!")
                else:
                    print("Пожалуйста, выберите от 1 до 5")
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def main_menu(self):
        """Главное меню игры"""
        print("🎮 ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'УГАДАЙ ЧИСЛО'!")
        
        while True:
            print("\n" + "="*30)
            print("ГЛАВНОЕ МЕНЮ")
            print("="*30)
            print("1. Начать игру")
            print("2. Инструкция")
            print("3. Статистика")
            print("4. Настройки сложности")
            print("5. Выйти")
            
            try:
                choice = input("\nВыберите действие (1-5): ").strip()
                
                if choice == '1':
                    self.start_game()
                elif choice == '2':
                    self.show_instructions()
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.change_difficulty()
                elif choice == '5':
                    print("Спасибо за игру! До свидания! 👋")
                    break
                else:
                    print("Пожалуйста, выберите от 1 до 5")
                    
            except KeyboardInterrupt:
                print("\n\nИгра завершена. До свидания! 👋")
                break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
    
    def start_game(self):
        """Запуск игрового процесса"""
        playing = True
        
        while playing:
            result = self.play_round()
            
            if result == 'QUIT':
                break
            elif result == 'RESTART':
                continue
            
            playing = self.ask_play_again()
        
        print("\nВозвращаемся в главное меню...")

def main():
    """Основная функция программы"""
    try:
        game = NumberGuessingGame()
        game.main_menu()
    except KeyboardInterrupt:
        print("\n\nИгра завершена. До свидания! 👋")
    except Exception as e:
        print(f"Произошла критическая ошибка: {e}")
        print("Пожалуйста, перезапустите программу.")

if __name__ == "__main__":
    main()