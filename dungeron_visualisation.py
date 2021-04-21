# use  Python ver 3.8.5
from typing import List, Text
from abc import ABC, abstractmethod
from termcolor import cprint, colored

RULES_MESSAGE = """
Правила игры
---------------------------------------------------------------
Вам необходимо добраться до Выхода (локация Hatch)
При этом успеть заработать 200 опыта
Всего дается 3 попытки 
Путь  есть  - Ищите !!
---------------------------------------------------------------
Если  устали - то при выборе действия можно сдаться - вводим 0

"""
EXIT_MESSAGE = 'Выход из игры'
TIME_MESSAGE = 'Вы провели в игре'
WRITE_RESULT_MESSAGE = 'Запись результатов прохождения в файл'
SURRENDERED_MESSAGE = 'Игрок Сдался'
TIME_IS_GONE_MESSAGE = 'Время вышло'
KILL_MESSAGE = 'Убил врага : '
NEXT_LOCATION_MESSAGE = 'Перешел в локацию : '
ATTEMPT_MESSAGE = 'Попытайтесь победить '
DIED_MESSAGE = 'Вы  Умерли'
STANDSTILL_MESSAGE = 'Выхода нет - тупик'
START_MESSAGE = 'Начинаем новую игру'
WIN_MESSAGE = 'Вы выиграли'
GAME_OVER_MESSAGE = 'Вы проиграли'
PLAYER_STATUS_MESSAGE = 'Статус Игрока :'
PLAYER_GET_USER_NAME_MESSAGE = 'Введите имя игрока : '
SMALL_EXPERIENCE_MESSAGE = 'Для Победы необходимо набрать 200 очков опыта за уничтожение врагов'


class Interface(ABC):
    """Интерфейс игры все переопредилить в наследниках"""

    @abstractmethod
    def display_get_main_menu(self, what: List) -> int:
        """Отобразить Глпаное меню и вернуть выбор пользователя"""
        pass

    @abstractmethod
    def display_standstill(self):
        """Отобразить сообщение тупик"""
        pass

    @abstractmethod
    def display_time(self, time_string: Text):
        """Отобразить сообщение о времени в в приложении"""
        pass

    @abstractmethod
    def display_write_to_file(self):
        """Отобразить сообщение о записи файла с результатами"""
        pass

    @abstractmethod
    def display_exit(self):
        """Отобразить сообщение Выход"""
        pass

    @abstractmethod
    def display_surrendered(self):
        """Отобразить сообщение Сдался"""
        pass

    @abstractmethod
    def display_small_experience_message(self):
        """Отобразить сообщение Мало опыта"""
        pass

    @abstractmethod
    def display_died_screen(self):
        """Отобразить сообщение о Смерти"""
        pass

    @abstractmethod
    def display_rules(self):
        """Отобразить правила игры"""
        pass

    @abstractmethod
    def display_start_screen(self):
        """Отобразить приветствие """
        pass

    @abstractmethod
    def display_win_screen(self):
        """Отобразить выигрыш"""
        pass

    @abstractmethod
    def display_end_game_screen(self):
        """Отобразить проигрыш"""
        pass

    @abstractmethod
    def display_time_is_gone_screen(self):
        """Отобразить Время вышло"""
        pass

    @abstractmethod
    def display_attempt_message(self, user_live: int):
        """Отобразить сообщение о попытке"""
        pass

    @abstractmethod
    def display_kill_message(self, add_experience: Text):
        """Отобразить сообщение о уничтожении моба"""
        pass

    @abstractmethod
    def display_next_location_message(self, location_name: Text):
        """Отобразить сообщение о переходе в следующую локацию"""
        pass

    @abstractmethod
    def display_player_status(self, user_status: Text):
        """
        Отобразить  статус игрока

        :param user_status: статус игрока
        :return:
        """
        pass

    @abstractmethod
    def get_player_action(self, possible_actions: List) -> int:
        """
        Вернет выбор действия игрока

        :param possible_actions: варианты действия
        :return: выбор дейстаия
        """
        pass

    @abstractmethod
    def get_user_name(self) -> Text:
        """
        Запросить и вернуть  имя игрока
        :return: имя Игрока
        """
        pass

    @abstractmethod
    def display_result(self, results):
        """
        Отобразить результат игрока
        :param results: список строк с результатами (журнал)
        """
        pass


class AnsiConsoleInterface(Interface):
    """Стандартный ANSI терминал """

    def get_user_name(self) -> Text:
        return input(PLAYER_GET_USER_NAME_MESSAGE)

    def display_rules(self):
        cprint(RULES_MESSAGE, color='green')

    def display_start_screen(self):
        cprint(START_MESSAGE, color='green')

    def display_win_screen(self):
        cprint(WIN_MESSAGE, color='green')

    def display_end_game_screen(self):
        cprint(GAME_OVER_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_player_status(self, user_status: Text):
        print(colored(PLAYER_STATUS_MESSAGE, color='green'), colored(user_status, color='magenta'))

    def get_player_action(self, possible_actions: List) -> int:
        menu = Menu(title='Выберите действие', menu_items=possible_actions)
        return menu.get_choice()

    def display_standstill(self):
        cprint(STANDSTILL_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_died_screen(self):
        cprint(DIED_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_attempt_message(self, user_live: Text):
        print(colored(ATTEMPT_MESSAGE, color='green'),
              colored(f'Осталось жизней {user_live}', color='magenta', attrs=['reverse', 'bold']))

    def display_kill_message(self, add_experience: Text):
        print(colored(KILL_MESSAGE, color='green'),
              colored(f'Заработал опыта : {add_experience}', color='magenta'))

    def display_next_location_message(self, location_name: Text):
        print(colored(NEXT_LOCATION_MESSAGE, color='green'), colored(location_name, color='magenta'))

    def display_time(self, time_string: Text):
        print(TIME_MESSAGE)
        print(time_string)

    def display_get_main_menu(self, what: List) -> int:
        menu = Menu(title='Главное меню', menu_items=what)
        return menu.get_choice()

    def display_time_is_gone_screen(self):
        cprint(TIME_IS_GONE_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_small_experience_message(self):
        cprint(SMALL_EXPERIENCE_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_surrendered(self):
        cprint(SURRENDERED_MESSAGE, color='red', attrs=['reverse', 'bold'])

    def display_exit(self):
        print(EXIT_MESSAGE)

    def display_result(self, results: List):
        for journal_message in results:
            print(journal_message)

    def display_write_to_file(self):
        print(WRITE_RESULT_MESSAGE)


class Menu:
    """Реалтзация меню"""

    def __init__(self, title: Text, menu_items: List):
        """
        Сооздание
        :param title: Заголовок меню
        :param menu_items: список пунктов
        :return : выбор игрока
        """
        self._menu_items = menu_items
        self.title = title

        self.set_menu_items(menu_items)

    def set_menu_items(self, menu_items: List):
        self._menu_items = menu_items

    def _print_menu(self):
        """отобразить"""
        menu_height = max(map(len, self._menu_items)) + 4
        cprint(f'{self.title}', color='green', attrs=['bold'])
        up_string = colored('┌───┬' + ('─' * menu_height) + '┐', color='magenta')
        down_string = colored('└───┴' + ('─' * menu_height) + '┘', color='magenta')
        print(up_string)
        for number, menu_item in enumerate(self._menu_items):
            vertical_symbol = colored('│', color='magenta')
            menu_number = colored(f' {number + 1} ', color='yellow')
            menu_line = colored(f' {menu_item:<{menu_height - 1}}', color='white', attrs=['reverse', 'bold'])
            print(vertical_symbol + menu_number + vertical_symbol + menu_line + vertical_symbol)
        print(down_string)

    def get_choice(self):
        """Запросить выбор"""
        while True:
            self._print_menu()
            choice = input('Ваш выбор (цифра из предложенного ):')
            try:
                choice = int(choice) - 1
            except ValueError:
                print('Должна быть цифра')
            else:
                if -1 <= choice < len(self._menu_items):
                    return choice
            print('Вы ошблись с вводом -  ещё раз')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(title="{self.title}",menu_items={self._menu_items})'


def get_interface() -> Interface:
    """
    Вернет интерфейс для игры
    :return: интерфейс
    """
    return AnsiConsoleInterface()
