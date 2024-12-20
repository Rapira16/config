# Эмулятор консоли
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
zip. Эмулятор должен работать в режиме CLI.

# Запуск
Перед запуском необходимо клонировать репозиторий в среду разработки

Запуск emulator.py: python emulator.py
```Bash
python emulator.py
```
Обязательно прописать путь к файловой системе в config.yaml

```Bash
pytest -v test_conf.py
```
Запуск тестов
# Необходимые библиотеки и их установка

```Bash
pip install -U pytest
```
библиотека для тестов

```Bash
pip install pyyaml
```
библитека yaml(для конфигурационных файлов)

```Bash
pip install lxml
```
для структуры файла  с расширением xml

# Команды
``` ls ``` - Список файлов и директорий

``` cd <path> ``` - Смена директории

``` exit ``` - Выход из эмулятора

``` find <file1> <file2> ... ``` - Вывод пути к файлу

``` mkdir <name> ``` - Создание директории

``` chmod  <number> <file1> <file2> ... ``` - Установка доступа

# Тесты
## ls
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/ls.png)
## cd
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/cd.png)
## exit
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/exit.png)
## find
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/find.png)
## mkdir
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/mkdir.png)
## chmod
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/chmod.png)
## Общие тесты через pytest
![](https://github.com/Rapira16/config/blob/main/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201/tests.png)
