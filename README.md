# dungeron

Игра - прохождение лабиринта  
Для запуска:  


python dungeon.py    



Библиотека : termcolor,decimal  


Карта подземелья представляет собой json-файл под названием rpg.json.  
Каждая локация в лабиринте описывается объектом, в котором находится единственный ключ  
с названием, соответствующем формату "Location_<N>_tm<T>"

где N - это номер локации (целое число), а T (вещественное число) - это время которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
 то он тратит на это 30000 секунд.
 По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
 Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
 которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
 которое потратит игрок для уничтожения данного монстра.
 Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
 Гарантируется, что в начале пути будет две локации и один монстр
 (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
  
 На прохождение игры игроку дается 123456.0987654321 секунд.
 Цель игры: за отведенное время найти выход ("Hatch")

 По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
 в каждую локацию можно попасть только один раз,
 и выйти из нее нельзя (то есть двигаться можно только вперед).

 Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
 Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
 готовый к следующей попытке (игра начинается заново).

