# use  Python ver 3.8.5
import builtins
from unittest import TestCase, main
from dungeron_visualisation import Menu, AnsiConsoleInterface,get_interface
from unittest.mock import patch

FIRST_OPTIONS = ['первый',
                 'второй',
                 'третий',
                 ]
SECOND_OPTIONS = ['первый 31',
                  'второй 25',
                  'третий 48',
                  ]


class TestAnsiConsoleInterfaceCase(TestCase):

    def setUp(self) -> None:
        self.term = AnsiConsoleInterface()


    def test_get_interface(self):
        interface = get_interface()
        self.assertIsInstance(interface,AnsiConsoleInterface)


    def test_get_user_name(self):
        with patch('builtins.input', return_value='test_user') as builtins.input:
            ret = self.term.get_user_name()
        self.assertEqual(ret, 'test_user', "Должна быть  'test_user' ")


class TestMenuCase(TestCase):
    """Проверки для класса Menu """

    def setUp(self) -> None:
        self.menu = Menu(title='Выберите вариант', menu_items=FIRST_OPTIONS)

    def test_one_menu(self) -> None:
        """Проверка создания меню пользователь вводит 1 """
        with patch('builtins.input', return_value='1') as builtins.input:
            what = self.menu.get_choice()
        self.assertEqual(what, 0, 'Должна быть 0')
        repr_string = repr(self.menu)
        self.assertEqual(repr_string, """Menu(title="Выберите вариант",menu_items=['первый', 'второй', 'третий'])""", 'Должна быть 0')

    def test_two_menu(self) -> None:
        """Проверка создания меню пользователь вводит 2 """
        self.menu.set_menu_items(SECOND_OPTIONS)
        with patch('builtins.input', return_value='2') as builtins.input:
            what = self.menu.get_choice()
        self.assertEqual(what, 1, 'Должна быть 1')


if __name__ == '__main__':
    main()
