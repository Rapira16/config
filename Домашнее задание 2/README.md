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

# Реализация

**extract_dependencies**

Для извлечения зависимых пакетов используем функцию **extract_dependencies**, которая принмает на вход путь к пакету NET. Далее В пакете ищем файл с расширением .nuspec, где содержатся метаданные о пакете (в том числе и зависимые пакеты). Далее уже в файле получаем ID и версию необходимого пакета. Далее проверяем, что пакет был посещен. Если не был посещен, то обходим его рекурсивно.

**generate_plantuml**

Для генерации кода на plantuml, используем функцию **generate_plantuml**, котрая на вход получает зависимости и основной пакет. Далее мы для основного пакета выводим по шаблону зависимые пакеты и возращаем зависимые корни.

**main**

В функции main мы парсим аргументы из командной строки - имя файла программы визулятора, путь к пакету и файл для вывода зависимостей на plantuml. 

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
Код на PlantUML для 1 теста.
```
@startuml
[newtonsoft] --> [Microsoft.CSharp 4.3.0]
[Microsoft.CSharp 4.3.0] --> [NETStandard.Library 1.6.1]
[Microsoft.CSharp 4.3.0] --> [System.ComponentModel.TypeConverter 4.3.0]
[Microsoft.CSharp 4.3.0] --> [System.Runtime.Serialization.Primitives 4.3.0]
[Microsoft.CSharp 4.3.0] --> [System.Runtime.Serialization.Formatters 4.3.0]
[Microsoft.CSharp 4.3.0] --> [System.Xml.XmlDocument 4.3.0]
[newtonsoft] --> [NETStandard.Library 1.6.1]
[NETStandard.Library 1.6.1] --> [System.ComponentModel.TypeConverter 4.3.0]
[NETStandard.Library 1.6.1] --> [System.Runtime.Serialization.Primitives 4.3.0]
[NETStandard.Library 1.6.1] --> [System.Runtime.Serialization.Formatters 4.3.0]
[NETStandard.Library 1.6.1] --> [System.Xml.XmlDocument 4.3.0]
[newtonsoft] --> [System.ComponentModel.TypeConverter 4.3.0]
[System.ComponentModel.TypeConverter 4.3.0] --> [System.Runtime.Serialization.Primitives 4.3.0]
[System.ComponentModel.TypeConverter 4.3.0] --> [System.Runtime.Serialization.Formatters 4.3.0]
[System.ComponentModel.TypeConverter 4.3.0] --> [System.Xml.XmlDocument 4.3.0]
[newtonsoft] --> [System.Runtime.Serialization.Primitives 4.3.0]
[System.Runtime.Serialization.Primitives 4.3.0] --> [System.Runtime.Serialization.Formatters 4.3.0]
[System.Runtime.Serialization.Primitives 4.3.0] --> [System.Xml.XmlDocument 4.3.0]
[newtonsoft] --> [System.Runtime.Serialization.Formatters 4.3.0]
[System.Runtime.Serialization.Formatters 4.3.0] --> [System.Xml.XmlDocument 4.3.0]
[newtonsoft] --> [System.Xml.XmlDocument 4.3.0]
@enduml
```
Далее идет визуальное отображение зависимотсей для 2-х пакетов
![](https://github.com/Rapira16/config/blob/main/Домашнее%20задание%202/test_package.png)
![](https://github.com/Rapira16/config/blob/main/Домашнее%20задание%202/test_2.png)
Тестирование отдельных функций
![](https://github.com/Rapira16/config/blob/main/Домашнее%20задание%202/tests.png)

