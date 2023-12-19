# Hitori Solver

v 1.0

**Авторы:** Анастасия Городничая, Виталий Карпов

## Описание:

Данное приложение способно решать головоломки "Hitori" разных форм, размеров и сложностей.

## Запуск:

Справка по запуску: ```python hitori_main.py -h```

Пример запуска: ```python hitori_main.py C:\...\example.txt```

### Формат входных данных:

В первой строке через пробел идут два натуральных числа m, n - ширина и высота головоломки.  
Далее, в следующих n строках через пробел идут по m чисел - значения клеток в головоломке.  

**Пример входных данных**:  
```4 3```  
```1 2 3 4```  
```2 3 4 1```  
```3 4 1 2```  

## Требования:

* Python версии не ниже 3.10
* Numpy версии не ниже 1.26.2

## Состав:

* Файл запуска: ```hitori_main.py```
* Модули Hitori: ```hitori/```
* Модули Command: ```command/``` *(реализация паттерна "Команда")*
* Тесты: ```tests/```
* Набор реальных головоломок разных уровней сложности: ```tests/test_files/real_puzzles```
