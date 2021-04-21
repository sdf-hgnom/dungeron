# use  Python ver 3.8.5
import builtins
from unittest import TestCase, main
from unittest.mock import patch, Mock

from dungeon_classes import *
from decimal import *


JSON_ONE = '{"Location_10_tm55100":["Mob_exp25_tm1","Mob_exp40_tm1"]}'


class TestGamaStage(TestCase):
    """Базовый для тестов состояний игры"""

    def setUp(self) -> None:
        self.game = Game()

    def set_user_name(self):
        """Создать пользователя + установить стпртовую локу"""
        self.game.transition_to(GameStart)
        with patch('builtins.input', return_value='test_user') as builtins.input:
            self.game._state.do()
        self.game.player.user_map.set_begin_location()
        self.game.player.count_live = 3
        self.game.player.remaining_time = '123456.0987654321'


class TestLocationCase(TestCase):
    """Проверки для класса Location """
    EXPECTED_LOCATION_ACTION = 'Переход в пещеру Location_0'

    def setUp(self) -> None:
        self.location = Location()

    def test_one_location_create(self):
        """Проаереа создания 1 локации + проверка ф-ции set_name"""
        self.location.set_name('Location_0_tm0')
        self.assertEqual(self.location.name, 'Location_0', 'Должна быть "Location_0"')
        self.assertEqual(self.location.data, '0', 'Должна быть "0"')

    def test_one_location_load(self):
        """Проаереа создания 1 локации из json строки """
        from_json = json.loads(JSON_ONE)
        self.location(from_json)
        self.assertEqual(self.location.name, 'Location_10', 'Должна быть "Location_10"')
        self.assertEqual(self.location.data, '55100', 'Должна быть "55100"')
        self.assertEqual(len(self.location.mobs), 2, 'Должна быть 2')

    def test_location_action(self):
        """Проверка ф-ции get_action"""
        self.location.set_name('Location_0_tm0')
        ret = self.location.get_action()
        self.assertEqual(ret, 'Переход в пещеру Location_0 за [0] опыта 0',
                         'Должна быть "Переход в пещеру Location_0 за [0] опыта 0"')


class TestEnemyCase(TestCase):
    """Проверки для класса Enemy """

    def setUp(self) -> None:
        self.mob = Enemy()

    def test_one_enemy_create(self):
        """Проверка срздания врага """
        self.mob.set_name('Mob_exp20_tm200')
        self.assertEqual(self.mob.name, 'Mob', 'Должна быть "Mob"')
        self.assertEqual(self.mob.data, '200', 'Должна быть "200"')
        self.assertEqual(self.mob.experience, '20', 'Должна быть "20"')
        repr_string = repr(self.mob)
        self.assertEqual(repr_string, 'Enemy(name=200)', 'Должна быть "Enemy(name=200)"')

    def test_get_action(self):
        """Проверка ф-ции get_action"""
        self.mob.set_name('Mob_exp20_tm200')
        ret = self.mob.get_action()
        self.assertEqual(ret, 'Убить монстра Mob за [200] опыта 20',
                         'Должна быть "Убить монстра Mob за [200] опыта 20"')


class TestEventsCase(TestCase):
    """Проверки для класса Event """

    def setUp(self) -> None:
        self.events = Events()
        action1 = EventAction(name='name1', experience='10', need_time='1')
        action2 = EventAction(name='name2', experience='20', need_time='2')
        action3 = EventAction(name='name3', experience='30', need_time='125.123456')
        self.events.append(action1)
        self.events.append(action2)
        self.events.append(action3)

    def test_repr(self):
        repr_string = repr(self.events)
        self.assertEqual(repr_string, 'Events with 3 EventAction', 'Должна быть "Events with 3 EventAction"')

    def test_add_action(self):
        """Проверка ф-ции add_action"""
        self.assertEqual(len(self.events), 3, 'Должна быть 3')

    def test_get_actions(self):
        """Проверка ф-ции get_actions"""
        actions = self.events.get_possible_actions
        self.assertEqual(len(actions), 3, 'Должна быть 3')
        self.assertEqual(actions[0], 'name1', 'Должна быть "name1"')
        self.assertEqual(actions[1], 'name2', 'Должна быть "name2"')
        self.assertEqual(actions[2], 'name3', 'Должна быть "name3"')

    def test_get_for_choice(self):
        """Проверка ф-ции get_for_choice"""
        actions = self.events[1]
        self.assertEqual(actions.name, 'name2', 'Должна быть "name1"')

    def test_delete(self):
        """Проверка ф-ции clear"""
        self.events.clear()
        action1 = EventAction(name='name1', experience='10', need_time='1')
        action2 = EventAction(name='name2', experience='10', need_time='1')
        self.events.append(action1)
        self.events.append(action2)
        self.assertEqual(len(self.events), 2, 'Должна быть 2')

        self.events.remove(action1)
        self.assertEqual(len(self.events), 1, 'Должна быть 1')

    def test_error_addition(self):
        """Проверка неверного обьекта добавления"""
        with self.assertRaises(ValueError):
            self.events.append('test')





class TestPlayerCase(TestCase):
    """Проверки для класса Player """
    FILE_TO_LOAD = '../rpg.json'
    EXPECTED_GET_STATUS = 'Игрок test21 : опыта добыто 0 осталось времени 123456.0987654321'

    def setUp(self) -> None:
        self.map = Map(input_file=TestMapCase.FILE_TO_LOAD)
        self.map.load()
        self.map.set_current_location(self.map.start_location)
        self.player = Player(name='test21', user_map=self.map)
        self.player.count_live = 3
        self.player.remaining_time = '123456.0987654321'

    def test_create(self):
        """Проверка создания"""
        self.assertEqual(self.player.name, 'test21', 'Должна быть "test21"')
        self.assertTrue(self.player.is_alive, 'Должна быть True')
        self.assertEqual(self.player.remaining_time, Decimal('123456.0987654321'), 'Должна быть "123456.0987654321"')
        self.assertEqual(self.player.user_map.current_location.name, 'Location_0', 'Должна быть "Location_0"')
        self.assertEqual(len(self.player.journal), 0, 'Должна быть 0')


    def test_add_journal_message(self):
        """Проверка добавления записи в журнал"""
        self.player.add_journal_message('First mess')
        self.player.experience = 100
        self.player.add_journal_message('Second mess')
        first_action: SagaAction = self.player.journal[0]
        second_action: SagaAction = self.player.journal[1]
        self.assertEqual(first_action.experience, 0, 'Должна быть 0')
        self.assertEqual(second_action.experience, 100, 'Должна быть 0')

    def test_get_status(self):
        """Проверка ф-ции get_status"""
        ret = self.player.get_status()
        self.assertEqual(ret, TestPlayerCase.EXPECTED_GET_STATUS,
                         f'Должна быть "Игрок test21 : опыта добыто 0 осталось времени 123456.0987654321"')

    def test_set_remaining_time(self):
        """Проверка установки remaining_time """
        self.player.remaining_time = 20
        self.assertEqual(self.player.remaining_time, 20, 'Должна быть 20')
        self.player.remaining_time = '123456.0987654321'
        self.assertEqual(self.player.remaining_time, Decimal('123456.0987654321'),
                         'Должна быть Decimal("123456.0987654321")')
        self.assertEqual(str(self.player.remaining_time), '123456.0987654321', 'Должна быть "123456.0987654321"')

    def test_is_alive(self):
        """Проверка ф-ции is_alive"""
        self.assertTrue(self.player.is_alive, 'Должна быть True')
        self.player.count_live = 0
        self.assertFalse(self.player.is_alive, 'Должна быть False')

    def test_do(self):
        """Проверка ф-ции do"""

        action = self.player.user_map.get_selected_action(what=0)
        self.player.do(what=action)
        self.assertEqual(str(self.player.remaining_time), '122416.0987654321', 'Должна быть "122416.0987654321"')
        self.assertEqual(self.player.experience, 0, 'Должна быть 0')


class TestMapCase(TestCase):
    """Проверки для класса Map """
    FILE_TO_LOAD = '../rpg.json'

    def setUp(self) -> None:
        self.map = Map(input_file=TestMapCase.FILE_TO_LOAD)
        self.map.load()
        self.map.set_current_location(what=self.map.start_location)

    def test_create_and_load(self):
        """Проверка создания + загрузка из json файла"""
        all_locations = self.map.get_locations_count(self.map.current_location)
        self.assertEqual(all_locations, 15, 'Должна быть 15')
        self.assertEqual(self.map.current_location.name, "Location_0", 'Должна быть "Location_0"')
        self.assertEqual(self.map.current_location.mobs[0].name, "Mob", 'Должна быть "Mob"')
        self.assertEqual(len(self.map.current_location.mobs), 1, 'Должна быть 1')
        tek = self.map.current_location.next_locations[0]
        self.assertEqual(tek.name, "Location_1", 'Должна быть "Location_1"')
        self.assertEqual(tek.mobs[0].name, "Mob", 'Должна быть "Mob"')
        self.assertEqual(len(tek.mobs), 2, 'Должна быть 2')


    def test_first_actions(self):
        """Проверка ф-ции get_possible_actions"""
        actions = self.map.get_possible_actions()
        self.assertEqual(len(actions), 3, 'Должна быть 2')
        self.assertEqual(actions[0], 'Переход в пещеру Location_1 за [1040] опыта 0',
                         "Должна быть 'Переход в пещеру Location_1за [1040] опыта 0'")
        self.assertEqual(actions[1], 'Переход в пещеру Location_2 за [33300] опыта 0',
                         "Должна быть 'Переход в пещеру Location_2 за [33300]опыта 0'")
        self.assertEqual(actions[2], 'Убить монстра Mob за [0] опыта 10',
                         "Должна быть 'Убить монстра Mob за [0] опыта 10'")


class TestSagaCase(TestCase):
    """Тесты для класса журнал игрока"""

    def setUp(self) -> None:
        self.saga = Saga()
        self.action = SagaAction(experience=10, location_name='test_loc', what_do='did something', player_name='test1')

    def test_good_append(self):
        """Проверка добавления правильного обьекта"""
        self.saga.append(self.action)
        self.assertEqual(len(self.saga), 1, 'Должен быть 1')

        self.assertIsInstance(self.action.action_datetime, datetime, 'Должен быть тип datetime.datetime')
        action_string = str(self.action)
        repr_saga_string = repr(self.saga)
        self.assertEqual(action_string[20:], 'Находясь в test_loc И имея 10 опыта Игрок test1 : did something')
        self.assertEqual(repr_saga_string, 'Saga with 1 SagaAction')

    def test_bad_append(self):
        """Проверка добавления не правильного обьекта"""
        with self.assertRaises(ValueError):
            self.saga.append('123')


class TestGameCase(TestGamaStage):
    """Проверки класса Game"""

    def test_play(self):
        self.game.transition_to(GameMainMenu)
        self.game.interface = Mock()
        with patch('builtins.input', return_value='4') as builtins.input:
            self.game.play()
        self.game.interface.display_time.assert_called_once()

    def test_game_start_state(self):
        """Проверка установки имени игрока"""
        self.set_user_name()
        self.assertEqual(self.game.player.name, 'test_user', "Должен быть 'test_user'")
        self.assertIsInstance(self.game._state, GameStart)

    def test_game_user_standstill(self):
        """Проверка перехода в состояние Тупик"""
        self.set_user_name()
        self.game.transition_to(GameUserDo)
        self.game.player.user_map.events.clear()
        with patch('builtins.input', return_value='1') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.assertEqual(new_state, GameStandstill)

    def test_game_player_surrendered(self):
        """Проверка перехода в состояние Игрок сдался"""
        self.set_user_name()
        self.game.player.user_map.set_begin_location()
        self.game.transition_to(GameUserDo)
        with patch('builtins.input', return_value='0') as builtins.input:
            new_state, new_action = self.game._state.do()
            self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GamePlayerSurrendered)

    def test_game_kill_mob(self):
        """Проверка перехода в состояние Убил врага"""
        self.set_user_name()
        self.game.player.user_map.set_begin_location()
        self.game.transition_to(GameUserDo)
        with patch('builtins.input', return_value='3') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.assertEqual(new_state, GameKillMob, 'Должен быть GameKillMob')

    def test_game_nex_location(self):
        """Проверка перехода в состояние переход в другую локу"""
        self.set_user_name()
        self.game.player.user_map.set_begin_location()
        self.game.transition_to(GameUserDo)
        with patch('builtins.input', return_value='1') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.assertEqual(new_state, GameNextLocation, 'Должен быть GameNextLocation')

    def test_game_time_is_gone(self):
        """Проверка перехода в состояние время вышло"""
        self.set_user_name()
        self.game.player.remaining_time = 0
        self.game.transition_to(GameUserDo)
        with patch('builtins.input', return_value='0') as builtins.input:
            new_state, new_action = self.game._state.do()
            self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameTimeIsGone)

    def test_game_over(self):
        """Проверка перехода в состояние проигрыш"""
        self.set_user_name()
        self.game.player.user_map.set_begin_location()
        self.game.player.count_live = 0
        self.game.player.remaining_time = '123456.0987654321'
        self.game.transition_to(GameAttempt)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameOver)

    def test_game_test_win(self):
        """Проверка перехода в состояние проверка выигрыша"""
        self.set_user_name()
        self.game.player.user_map.set_win_location()
        self.game.player.user_map.set_current_location(self.game.player.user_map.pre_win_location)
        actions = self.game.player.user_map.events
        action_to_win = actions[0]
        self.game.player.count_live = 1
        self.game.player.remaining_time = '123456.0987654321'
        self.game.transition_to(GameNextLocation, action_to_win)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameTestWin)

    def test_game_win(self):
        """Проверка перехода в состояние Выиграл"""
        self.set_user_name()
        self.game.player.count_live = 1
        self.game.player.remaining_time = '123456.0987654321'
        self.game.player.experience = 201
        self.game.transition_to(GameTestWin)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameWin)

    def test_game_small_experience(self):
        """Проверка перехода в состояние Мало опыта"""
        self.set_user_name()
        self.game.player.count_live = 1
        self.game.player.remaining_time = '123456.0987654321'
        self.game.player.experience = 0
        self.game.transition_to(GameTestWin)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameSmallExperience)

    def test_game_kill_mob_state(self):
        """Проверка работы Убил моба"""
        self.set_user_name()
        self.game.player.experience = 0
        self.game.player.user_map.set_begin_location()
        actions = self.game.player.user_map.events
        action_for_run = actions[2]
        self.game.transition_to(GameKillMob, action_for_run)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameUserDo)
        self.assertEqual(self.game.player.experience, 10, "Должно быть 10")

    def test_game_next_location(self):
        self.set_user_name()
        self.game.player.user_map.set_begin_location()
        actions = self.game.player.user_map.events
        action_for_run = actions[0]
        self.game.transition_to(GameNextLocation, action_for_run)
        new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertIsInstance(self.game._state, GameUserDo)
        self.assertEqual(self.game.player.user_map.current_location.name, 'Location_1', "Должно быть 'Location_1")


class TestGameMainMenu(TestCase):
    """Проверка класса состояния GameMainMenu"""

    def setUp(self) -> None:
        self.game = Game()

    def test_main_menu_start(self):
        """Переход в Start"""
        self.game.transition_to(GameMainMenu)
        with patch('builtins.input', return_value='1') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertEqual(new_state, GameStart)

    def test_main_menu_rules(self):
        """Переход в показ правил"""
        self.game.transition_to(GameMainMenu)
        with patch('builtins.input', return_value='2') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.game.transition_to(new_state, new_action)
        self.assertEqual(new_state, GameRules)

    def test_main_menu_result(self):
        """Переход в показ результатов"""
        self.game.transition_to(GameMainMenu)
        with patch('builtins.input', return_value='3') as builtins.input:
            new_state, new_action = self.game._state.do()
            self.game.transition_to(new_state, new_action)
        self.assertEqual(new_state, GameResult)

    def test_main_menu_exit1(self):
        """Выход штатно"""
        self.game.transition_to(GameMainMenu)
        with patch('builtins.input', return_value='4') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.assertIsNone(new_state, "Должен быть None")

    def test_main_menu_exit2(self):
        """Выход отказ"""
        self.game.transition_to(GameMainMenu)
        with patch('builtins.input', return_value='0') as builtins.input:
            new_state, new_action = self.game._state.do()
        self.assertIsNone(new_state, "Должен быть None")


class TestGameWinCase(TestGamaStage):
    """Полверка класса GameWin"""

    def test_game_win_do(self):
        """Проверка ф-ции do"""
        self.set_user_name()
        self.game.transition_to(GameWin)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_win_screen.assert_called_once()
        self.assertEqual(new_state, GameWriteResult, "Должен быть GameWriteResult")


class TestGameTimeIsGone(TestGamaStage):
    """Проверка Состояния GameTimeIsGone"""

    def test_game_time_is_gone_do(self):
        """Проверка ф-ции do"""
        self.set_user_name()
        self.game.transition_to(GameTimeIsGone)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_time_is_gone_screen.assert_called_once()
        self.assertEqual(new_state, GameUserDied, "Должен быть GameUserDied")


class TestGamePlayerSurrendered(TestGamaStage):
    """Проверка Состояния GamePlayerSurrendered"""

    def test_game_player_surrendered_do(self):
        self.set_user_name()
        self.game.transition_to(GamePlayerSurrendered)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_surrendered.assert_called_once()
        self.assertEqual(new_state, GameMainMenu, "Должен быть GameMainMenu")


class TestGameSmallExperience(TestGamaStage):
    """Проверка Состояния GameSmallExperience"""

    def test_game_small_experience_do(self):
        self.set_user_name()
        self.game.transition_to(GameSmallExperience)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_small_experience_message.assert_called_once()
        self.assertEqual(new_state, GameUserDied, "Должен быть GameUserDied")


class TestGameResult(TestGamaStage):
    """Проверка Состояния GameResult"""

    def test_do(self):
        self.set_user_name()
        self.game.transition_to(GameResult)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_result.assert_called_once()
        self.assertEqual(new_state, GameMainMenu, "Должен быть GameMainMenu")


class TestGameGameOver(TestGamaStage):
    """Проверка Состояния GameGameOver"""

    def test_game_small_experience_do(self):
        self.set_user_name()
        self.game.transition_to(GameOver)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_end_game_screen.assert_called_once()
        self.assertEqual(new_state, GameWriteResult, "Должен быть GameWriteResult")


class TestGameRules(TestGamaStage):
    """Проверка Состояния GameRules"""

    def test_game_small_experience_do(self):
        self.game.transition_to(GameRules)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_rules.assert_called_once()
        self.assertEqual(new_state, GameMainMenu, "Должен быть GameMainMenu")


class TestGameStandstill(TestGamaStage):
    """Проверка Состояния GameStandstill"""

    def test_game_small_experience_do(self):
        self.set_user_name()
        self.game.transition_to(GameStandstill)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_standstill.assert_called_once()
        self.assertEqual(new_state, GameUserDied, "Должен быть GameMainMenu")


class TestGameAttempt(TestGamaStage):
    """Проверка Состояния GameAttempt"""

    def test_game_small_experience_do_good(self):
        self.set_user_name()
        self.game.transition_to(GameAttempt)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_attempt_message.assert_called_once()
        self.assertEqual(new_state, GameUserDo, "Должен быть GameUserDo")

    def test_game_small_experience_do_bad(self):
        self.set_user_name()
        self.game.player.count_live = 0
        self.game.transition_to(GameAttempt)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.assertEqual(new_state, GameOver, "Должен быть GameOver")


class TestGameExit(TestGamaStage):
    """Проверка Состояния GameExit"""

    def test_game_small_experience_do(self):
        self.game.transition_to(GameExit)
        self.game.interface = Mock()
        new_state, new_action = self.game._state.do()
        self.game.interface.display_exit.assert_called_once()
        self.assertIsNone(new_state, "Должен быть None")


class TestGameUserDied(TestGamaStage):
    """Проверка Состояния GameUserDied"""

    def test_game_small_experience_do(self):
        self.set_user_name()
        self.game.transition_to(GameUserDied)
        self.game.interface = Mock()

        new_state, new_action = self.game._state.do()
        self.game.interface.display_died_screen.assert_called_once()
        self.assertEqual(new_state, GameAttempt, "Должен быть GameAttempt")
        self.assertEqual(self.game.player.count_live, 2, "Должен быть 2")


class TestGameWriteResult(TestGamaStage):
    """Проверка Состояния GameWriteResult"""

    def test_game_write_result_do(self):
        """Проверка ф-ции do"""
        self.set_user_name()
        self.game.transition_to(GameWriteResult)
        state_repr = repr(self.game._state)
        self.game.interface = Mock()
        self.game.player.add_journal_message('Test')
        new_state, new_action = self.game._state.do()
        self.game.interface.display_write_to_file.assert_called_once()
        self.assertEqual(new_state, GameMainMenu, "Должен быть GameMainMenu")
        self.assertEqual(state_repr, 'GameWriteResult()', "Должен быть 'GameWriteResult()'")


if __name__ == '__main__':
    main()
