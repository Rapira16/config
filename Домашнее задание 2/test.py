import pytest
import zipfile
from io import BytesIO
from main import extract_dependencies, generate_plantuml  # Замените 'main' на имя вашего модуля


@pytest.fixture
def nupkg_content():
    # Создаем временный .nupkg файл для тестов
    content = BytesIO()
    with zipfile.ZipFile(content, 'w') as z:
        nuspec_content = '''<?xml version="1.0"?>
        <package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">
            <metadata>
                <id>TestPackage</id>
                <version>1.0.0</version>
                <dependencies>
                    <dependency id="DependencyA" version="1.0.0" />
                    <dependency id="DependencyB" version="2.0.0" />
                </dependencies>
            </metadata>
        </package>
        '''
        z.writestr('TestPackage.nuspec', nuspec_content)
        # Остальной код для зависимостей (если есть)
    content.seek(0)  # Сбрасываем указатель на начало
    return content


def test_extract_dependencies(nupkg_content):
    # Тестируем функцию extract_dependencies и выводим зависимости
    dependencies = extract_dependencies(nupkg_content)
    assert dependencies == {
        'DependencyA': '1.0.0',
        'DependencyB': '2.0.0'
    }, "Зависимости не соответствуют ожидаемым!"

    # Выводим зависимости на экран при успешном тесте
    print("Тест extract_dependencies пройден успешно!")
    print("Зависимости:", dependencies)


def test_generate_plantuml():
    # Тестируем функцию generate_plantuml
    dependencies = {
        'DependencyA': '1.0.0',
        'DependencyB': '2.0.0',
        'InnerDependencyA': '1.0.0'
    }
    main_package = 'TestPackage'
    expected_plantuml = (
        "@startuml\n"
        "[TestPackage] --> [DependencyA 1.0.0]\n"
        "[DependencyA 1.0.0] --> [DependencyB 2.0.0]\n"
        "[DependencyA 1.0.0] --> [InnerDependencyA 1.0.0]\n"
        "[TestPackage] --> [DependencyB 2.0.0]\n"
        "[DependencyB 2.0.0] --> [InnerDependencyA 1.0.0]\n"
        "[TestPackage] --> [InnerDependencyA 1.0.0]\n"
        "@enduml"
    )
    plantuml_code = generate_plantuml(dependencies, main_package)

    # Сравниваем с ожидаемым результатом
    assert plantuml_code.strip() == expected_plantuml.strip(), "Сгенерированный код не соответствует ожидаемому!"

    # Выводим сгенерированный код для отладки при успешном тесте
    print("Тест generate_plantuml пройден успешно!")
    print("Сгенерированный код PlantUML:\n", plantuml_code)
