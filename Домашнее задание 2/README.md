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
![](https://github.com/Rapira16/config/blob/main/Домашнее%20задание%202/test_package.png)

