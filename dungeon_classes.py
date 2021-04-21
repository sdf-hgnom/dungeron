# use  Python ver 3.8.5
"""Модуль с классами движка для игры Dungeon"""
import json
import csv
import time
from abc import ABC, abstractmethod

from collections import UserList
from datetime import datetime
from typing import List, Text, ClassVar, Optional, Dict, Tuple, Any
from decimal import *

from dungeron_visualisation import get_interface


class DungeonCsv(csv.Dialect):
    """Describe the  CSV формат для игры dungeon  files."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_NONNUMERIC


class Action:
    """базовый для сущностей с которыми можно что-то сделать
    self.name - название сущьности
    self.data - данные  сущности
    """

    def __init__(self):
        self.name: Text = ''
        self.data: Text = ''

    def set_name(self, name: Text) -> None:
        """Необходимо переопределить в наследниках что-бы установить правильные данные сущьности"""
        raise NotImplementedError

    def get_action(self) -> Text:
        """Необходимо переопределить в наследниках что-б вернул  описание дейстаия над сущьностью"""
        raise NotImplementedError


class Enemy(Action):
    """Класс врагов"""

    def __init__(self):
        super().__init__()
        self.experience: Text = ''
        self.data: Text = ''
        # self.name = ''

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}(name={self.data})'

    def set_name(self, name: Text) -> None:
        """Установить параметры моба (зашифрованы в имени)"""
        mob_name, mob_experience, mob_data = name.split('_')
        self.name = mob_name
        self.data = mob_data[2:]
        self.experience = mob_experience[3:]

    def get_action(self) -> Text:
        """Вернет строчку - что можно сделать"""
        return f'Убить монстра {self.name} за [{self.data}] опыта {self.experience}'


class EventAction:
    """Класс параметров действия"""

    def __init__(self, name, experience, need_time, origin=None):
        """
        Создание действия
        :param name: Имя действия
        :param experience: Сколько опыта за действие
        :param need_time: Сколько времени на действие
        :param origin:  сам элемент действия
        """
        self.name = name
        self.origin = origin
        self.experience: int = int(experience)
        self.need_time: Text = need_time

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}(' \
               f'{self.name}),' \
               f'{self.experience},' \
               f'{self.need_time})'


class Events(UserList):
    """Перечень событий (действий)"""

    def __repr__(self):
        return f'{self.__class__.__name__} with {len(self.data)} EventAction'

    def append(self, item) -> None:
        if not hasattr(item, 'name'):
            raise ValueError(f'{self.__class__.__name__} : For normal work object must has attribute named "name"')
        super().append(item)

    @property
    def get_possible_actions(self):
        """Вернет список действий"""
        current_possible_actions = []
        for action in self.data:
            current_possible_actions.append(action.name)
        return current_possible_actions


class Location(Action):
    """Одна локация нп карте
       self.mobs : список  мобов в локации
       self.next_locations : список дверей в другие локации
       self.data : время перехода из текущей локации
    """

    def __init__(self):

        super().__init__()
        self.mobs: List = []
        self.next_locations: List[Location] = []

    def set_name(self, name: Text) -> None:
        """Установить имя локации и время перехода в нее"""
        location_name, location_data = name.split('tm')
        self.name = location_name[:-1]
        self.data = location_data

    def get_action(self) -> Text:
        return f'Переход в пещеру {self.name} за [{self.data}] опыта {0}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __call__(self, *args, **kwargs):
        """Метод обеспечит загрузку локаций из словаря со списком локаций"""
        input_data = None
        input_data_in_location = None

        if args:
            input_data = args[0]
        if isinstance(input_data, dict):
            for key, data in input_data.items():
                self.set_name(key)
                input_data_in_location = data
        elif isinstance(input_data, str):
            self.data = input_data
            input_data_in_location = []

        else:
            input_data_in_location = input_data
        for item in input_data_in_location:
            if isinstance(item, str) and (item.startswith('Mob') or item.startswith('Boss')):
                new_enemy = Enemy()
                new_enemy.set_name(name=item)
                self.mobs.append(new_enemy)
            else:
                for new_location_name, new_location_data in item.items():
                    new_location = Location()
                    new_location.set_name(name=new_location_name)
                    self.next_locations.append(new_location)
                    new_location(new_location_data)


class SagaAction:
    """Класс для 1 строчки саги
    action_datetime  - время этого действия будет зафиксированно при добавлении в сагу
    """
    TIME_FORMAT = '%d.%m.%Y %H:%M:%S'

    def __init__(self, experience: int, location_name: Text, what_do: Text, player_name: Text):
        """
        Создание
        :param experience: текущий опыт
        :param location_name: текущая локация
        :param player_name : имя игрока
        :param what_do: что сделал
        """
        self.action_datetime: datetime = datetime.now()
        self.location_name: Text = location_name
        self.experience: int = experience
        self.player_name: Text = player_name
        self.what_do: Text = what_do

    def get_for_csv(self) -> Dict:
        """Вернет строчку в формате csv.DictWriter"""
        return {'current_location': f"{self.location_name}",
                'current_experience': self.experience,
                'current_date': f"{datetime.strftime(self.action_datetime, self.TIME_FORMAT)}",
                'current_what_do': f'{self.what_do}',
                }

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}(' \
               f'{self.location_name},' \
               f'{self.experience},' \
               f'{self.what_do})'

    def __str__(self) -> Text:
        return f'{datetime.strftime(self.action_datetime, self.TIME_FORMAT)} ' \
               f'Находясь в {self.location_name} ' \
               f'И имея {self.experience} опыта ' \
               f'Игрок {self.player_name} : {self.what_do}'


class Saga(UserList):
    """Журнал действий игрока с фиксацией времени"""

    def __repr__(self):
        return f'{self.__class__.__name__} with {len(self.data)} SagaAction'

    def append(self, item) -> None:
        if not hasattr(item, 'action_datetime'):
            raise ValueError(f'{self.__class__.__name__} : '
                             f'For normal work object must has attribute named "action_datetime"')
        item.action_datetime = datetime.now()
        super().append(item)


class Map:
    """Карта локаций которая будет выданна игроку"""

    def __init__(self, input_file: Text):
        """
        Создание
        :param input_file: json файл с локациями
        """
        self.input_file: Text = input_file
        self.current_location: Optional[Location] = None
        self.pre_win_location: Optional[Location] = None
        self.events: Optional[Events] = None
        self.start_location: Optional[Location] = None

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}({self.input_file})'

    @staticmethod
    def get_locations_count(start: Location) -> int:
        """Вернет кол-во локаций на карте"""
        all_count = 0
        if not start.next_locations:
            return 0
        else:
            for location in start.next_locations:
                all_count += Map.get_locations_count(location)
                all_count += 1

        return all_count

    def set_win_location(self, start: Optional[Location] = None) -> None:
        """
        Установит локацию в которой находится победа (нужно для тестов)

        :param start: begin location
        """
        if start is None:
            start = self.start_location
        for location in start.next_locations:
            for test_location in location.next_locations:
                if test_location.name == Game.NAME_WIN_LOCATION:
                    self.pre_win_location = location
                else:
                    self.set_win_location(start=location)

    def set_current_location(self, what: Location):
        """Установить текущую локацию на карте + создание возможных действий в этой локации"""
        self.current_location = what
        self.events.clear()
        for location in what.next_locations:
            new_action = EventAction(name=location.get_action(), need_time=location.data, experience=0, origin=location)
            self.events.append(new_action)
        for mob in what.mobs:
            new_action = EventAction(name=mob.get_action(), experience=mob.experience, need_time=mob.data, origin=mob)
            self.events.append(new_action)

    def set_begin_location(self):
        """Сбросить в начало """
        self.set_current_location(what=self.start_location)

    def load(self):
        """Загрузить локации из json файла"""
        start_location: Location = Location()

        with open(self.input_file, 'rt', encoding='utf-8') as file:
            loaded_from_json_file = json.load(file)
        start_location(loaded_from_json_file)
        self.events = Events()
        self.start_location = start_location

    def get_possible_actions(self) -> List:
        """Вернет перечень возможных действий в текущей локации"""

        return self.events.get_possible_actions

    def get_selected_action(self, what: int) -> EventAction:
        """Вернет действие по индексу"""
        return self.events[what]


class Player:
    """Класс Игрока"""

    def __init__(self, name: Text, user_map: Map) -> None:
        """
        Создание
        :param name:  имя игрока
        :param user_map: карта игрока
        """
        self.name: Text = name
        self.user_map: Map = user_map
        self._count_live: int = 0
        self._remaining_time = Decimal()
        self.experience: int = 0
        self.journal: Saga = Saga()

    @property
    def remaining_time(self):
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, value):
        if isinstance(value, Decimal):
            self._remaining_time = value
        else:
            self._remaining_time = Decimal(value)

    @property
    def count_live(self):
        return self._count_live

    @count_live.setter
    def count_live(self, value):
        self._count_live = value

    @property
    def is_alive(self):
        """Может-ли игрок играть"""
        return self._count_live > 0

    @property
    def is_has_time(self):
        """Есть-ли у игрока время"""
        return self._remaining_time > 0

    def add_journal_message(self, message: Text):
        """Добавить новую запись в журнал"""
        new_item = SagaAction(experience=self.experience,
                              location_name=self.user_map.current_location.name,
                              what_do=message, player_name=self.name)
        self.journal.append(new_item)

    def do(self, what: EventAction) -> None:
        """Фиксация результатов действия игрока"""
        if isinstance(what.origin, Location):
            self.remaining_time -= Decimal(what.need_time)
        else:
            self.experience += int(what.experience)
            self.remaining_time -= Decimal(what.need_time)

    def get_status(self) -> Text:
        """Вернет описание состояния игрока"""
        return f'Игрок {self.name} : опыта добыто {self.experience} осталось времени {str(self.remaining_time)}'

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}({self.name})'


class Game:
    """Основной класс игры по патерну Состояние"""
    MAX_PLAYER_LIVE = 3
    EXPERIENCE_TO_WIN = 200
    REMAINING_TIME = '123456.0987654321'
    FILE_TO_LOAD = 'rpg.json'
    FILE_TO_WRITE = 'dungeon.csv'
    WRITE_FIELDS = ['current_location', 'current_experience', 'current_date', 'current_what_do']
    NAME_WIN_LOCATION = 'Hatch'
    MAIN_MENU_ITEM = ['Новая игра ',
                      'Показать описание',
                      'Показать результаты',
                      'Выход',
                      ]
    _state = None

    def __init__(self):
        self.interface = get_interface()
        self.player: Optional[Player] = None
        self.game_start: float = time.monotonic()

    def transition_to(self, state: ClassVar, action: Optional[EventAction] = None):
        """
        Переход в другое состояние
        :param state: новое состояние
        :param action: Действие для этого состояния
        :return:
        """
        next_state = state(action=action)
        self._state = next_state
        self._state.context = self

    def play(self):
        """Основной цикл игры"""
        while True:
            next_state, next_state_action = self._state.do()
            if next_state is not None:
                self.transition_to(state=next_state, action=next_state_action)
            else:
                break
        elapsed = time.monotonic() - self.game_start
        play_time = datetime.strftime(datetime.utcfromtimestamp(elapsed), '%H:%M:%S')
        self.interface.display_time(time_string=play_time)


class State(ABC):
    """Абстрактный класс-состояние"""

    def __init__(self):
        self._context: (Game, None) = None

    def __repr__(self) -> Text:
        return f'{self.__class__.__name__}()'

    @property
    def context(self) -> Game:
        return self._context

    @context.setter
    def context(self, context: Game) -> None:
        self._context = context

    @abstractmethod
    def do(self) -> Tuple[Any, Any]:
        """Сделать необходимые дейстаия на данном этапе"""
        pass


class GameStart(State):
    """Состояние Начало игры"""

    def __init__(self, action: Optional[EventAction] = None):
        super().__init__()
        self.action: Optional[EventAction] = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_start_screen()
        user_map = Map(input_file=Game.FILE_TO_LOAD)
        user_map.load()
        user_name = self.context.interface.get_user_name()
        new_user = Player(name=user_name, user_map=user_map)
        new_user.count_live = Game.MAX_PLAYER_LIVE
        self.context.player = new_user
        return GameAttempt, self.action


class GameAttempt(State):
    """Состояние Новая попытка"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        if self.context.player.is_alive:
            self.context.interface.display_attempt_message(user_live=self.context.player.count_live)
            self.context.player.remaining_time = Game.REMAINING_TIME
            self.context.player.experience = 0
            self.context.player.user_map.set_begin_location()
            self.context.player.add_journal_message(f'Игрок предротнял новую попытку пройти игру')
            return GameUserDo, self.action
        else:
            return GameOver, self.action


class GameStandstill(State):
    """Состояние Тупик"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_standstill()
        self.context.player.add_journal_message(f'Игрок зашел в тупик')
        return GameUserDied, self.action


class GameRules(State):
    """Состояние Показать Правила"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_rules()
        return GameMainMenu, self.action


class GameOver(State):
    """Состояние Проигрыш"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_end_game_screen()
        self.context.player.add_journal_message(f'Игрок истратил все жизни но так и не смог найти выход')
        return GameWriteResult, self.action


class GameWriteResult(State):
    """Состояние записать в файл журнал"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        csv.register_dialect("dungeon", DungeonCsv)
        self.context.interface.display_write_to_file()
        with open(Game.FILE_TO_WRITE, 'at', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=Game.WRITE_FIELDS, delimiter=',', dialect='dungeon')
            writer.writeheader()
            for journal_message in self.context.player.journal:
                writer.writerow(journal_message.get_for_csv())

        return GameMainMenu, self.action


class GameResult(State):
    """Состояние Показать журнал"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        if self.context.player is not None:
            self.context.interface.display_result(results=self.context.player.journal)
        return GameMainMenu, self.action


class GameExit(State):
    """Состояние Выход"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.game_end_datetime = datetime.now()
        self.context.interface.display_exit()
        return None, self.action


class GameMainMenu(State):
    """Состояние Главное меню"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        player_choice = self.context.interface.display_get_main_menu(what=Game.MAIN_MENU_ITEM)
        if player_choice == 0:
            return GameStart, self.action
        elif player_choice == 1:
            return GameRules, self.action
        elif player_choice == 2:
            return GameResult, self.action
        else:
            return None, self.action


class GameWin(State):
    """Состояние Победил"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_win_screen()
        self.context.player.add_journal_message(f'Игрок нашел выход и победил')
        return GameWriteResult, self.action


class GameTimeIsGone(State):
    """Состояние Время вышло"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_time_is_gone_screen()
        self.context.player.add_journal_message(f'Вышло время - Вы тонете')
        return GameUserDied, self.action


class GamePlayerSurrendered(State):
    """Состояние Игрок сдался"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_surrendered()
        self.context.player.add_journal_message(f'Игроку надоели пещеры и ор сдался')
        return GameMainMenu, self.action


class GameUserDo(State):
    """Состояние выбор пользователя"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.player.add_journal_message(f'Игрок раздумывает - что предпринять')
        if not self.context.player.is_has_time:
            return GameTimeIsGone, self.action
        self.context.interface.display_player_status(self.context.player.get_status())
        actions = self.context.player.user_map.get_possible_actions()
        if len(actions) == 0:
            return GameStandstill, self.action
        player_choice = self.context.interface.get_player_action(possible_actions=actions)
        if player_choice == -1:
            return GamePlayerSurrendered, None
        selected_actions: EventAction = self.context.player.user_map.get_selected_action(what=player_choice)
        if isinstance(selected_actions.origin, Location):
            return GameNextLocation, selected_actions
        else:
            return GameKillMob, selected_actions


class GameKillMob(State):
    """Состояние убил моба"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_kill_message(add_experience=self.action.experience)
        self.context.player.do(what=self.action)
        self.context.player.user_map.events.remove(self.action)
        self.action = None
        self.context.player.add_journal_message(f'Игрок убил врага')
        return GameUserDo, self.action


class GameNextLocation(State):
    """Состояние переход в следующую локацию"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_next_location_message(location_name=self.action.origin.name)
        self.context.player.add_journal_message(f'Игрок перешел в другую пещеру')
        if self.action.origin.name == Game.NAME_WIN_LOCATION:
            self.action = None
            return GameTestWin, self.action
        self.context.player.do(what=self.action)
        self.context.player.user_map.set_current_location(what=self.action.origin)
        self.action = None

        return GameUserDo, self.action


class GameSmallExperience(State):
    """Состояние Мало опыта"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_small_experience_message()
        self.context.player.add_journal_message(f'Игрок добрался до выхода - но ему не хватило опыта')
        return GameUserDied, self.action


class GameTestWin(State):
    """Состояние Проверка выигрыша"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        if self.context.player.experience >= Game.EXPERIENCE_TO_WIN:
            return GameWin, self.action
        return GameSmallExperience, self.action


class GameUserDied(State):
    """Состояние Игрок умер"""

    def __init__(self, action: EventAction = None):
        super().__init__()
        self.action: EventAction = action

    def do(self) -> Tuple[Any, Any]:
        self.context.interface.display_died_screen()
        self.context.player.count_live -= 1
        self.context.player.add_journal_message(f'Игрок умер')
        return GameAttempt, self.action
