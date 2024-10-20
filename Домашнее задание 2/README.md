# Зависимости пакета
Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.
139
Зависимости определяются по имени пакета платформы .NET (nupkg). Для
описания графа зависимостей используется представление PlantUML.
Визуализатор должен выводить результат на экран в виде кода.
Ключами командной строки задаются:
• Путь к программе для визуализации графов.
• Имя анализируемого пакета.
• Путь к файлу-результату в виде кода.

# Запуск
Перед запуском необходимо клонировать репозиторий в среду разработки
Далее для правильной работы программы необходимо установить пакет с расширением nupkg с официального сайта. В примере используется пакет Newtonsoft.Json (ссылка на скачивание https://www.nuget.org/packages/Newtonsoft.Json/#readme-body-tab)

Далее запустить файл main.py по нижепредставленному шаблону

В шаблоне:

main.py - программу визуализатор

/путь/к/файлу/.nupkg - путь к уже установленному пакету с расширением .nupkg

output.puml - код для визуализации графа зависимостей

```Bash
python main.py /путь/к/файлу/.nupkg output.puml
```

Дополнительные библиотеки устанавливать не требуется.

# Тестирование
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

