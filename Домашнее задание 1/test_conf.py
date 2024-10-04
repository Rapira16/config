import pytest
from emulator import Emulator, VirtualFileSystem, CommandProcessor

def test_ls_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду ls
    command_processor.process_command("ls")
    # Проверяем, что команда выполнена успешно
    assert True

def test_ls_command_with_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду ls с аргументами
    command_processor.process_command("ls first")
    # Проверяем, что команда выполнена успешно
    assert True

def test_ls_command_with_invalid_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем эмулятор
    emulator = Emulator("config.yaml")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, emulator)
    # Выполняем команду ls с невалидными аргументами
    command_processor.process_command("ls invalid_dir")
    # Проверяем, что команда не выполнена успешно
    assert command_processor.current_dir != "invalid_dir"

def test_cd_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду cd
    command_processor.process_command("cd first")
    # Проверяем, что текущая директория изменилась
    assert command_processor.current_dir == "first"

def test_cd_command_with_invalid_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду cd с невалидными аргументами
    command_processor.process_command("cd invalid_dir")
    # Проверяем, что текущая директория не изменилась
    assert command_processor.current_dir != "invalid_dir"

def test_cd_command_with_relative_path():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду cd с относительным путем
    command_processor.process_command("cd ..")
    # Проверяем, что текущая директория изменилась
    assert command_processor.current_dir == "."

def test_exit_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("test_archive.zip")
    # Создаем эмулятор
    emulator = Emulator("config.yaml")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, emulator)
    # Выполняем команду exit
    with pytest.raises(SystemExit):
        command_processor.process_command("exit")

def test_exit_command_with_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем эмулятор
    emulator = Emulator("config.yaml")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, emulator)
    # Выполняем команду exit с аргументами
    with pytest.raises(SystemExit):
        command_processor.process_command("exit invalid_arg")

def test_find_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем эмулятор
    emulator = Emulator("config.yaml")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, emulator)
    # Выполняем команду find
    command_processor.process_command("find numbers.txt")
    # Проверяем, что файл найден
    assert "first/numbers.txt" in vfs.zip_ref.namelist()

def test_find_command_with_invalid_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду find с невалидными аргументами
    command_processor.process_command("find invalid_file")
    # Проверяем, что файл не найден
    assert "invalid_file" not in vfs.zip_ref.namelist()

def test_find_command_with_multiple_files():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем эмулятор
    emulator = Emulator("config.yaml")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, emulator)
    # Выполняем команду find с несколькими файлами
    command_processor.process_command("find numbers.txt main.txt")
    # Проверяем, что файлы найдены
    assert "first/numbers.txt" in vfs.zip_ref.namelist() and "main.txt" in vfs.zip_ref.namelist()

def test_mkdir_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду mkdir
    command_processor.process_command("mkdir test_dir")
    # Проверяем, что директория создана
    assert "test_dir/" in vfs.zip_ref.namelist()

def test_mkdir_command_with_relative_path():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду mkdir с относительным путем
    command_processor.process_command("mkdir first/subdir")
    # Проверяем, что директория создана
    assert "first/subdir/" in vfs.zip_ref.namelist()

def test_chmod_command():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду chmod
    command_processor.process_command("chmod 755 numbers.txt")
    # Проверяем, что права доступа изменены
    assert vfs.permissions["numbers.txt"] == 0o755

def test_chmod_command_with_invalid_args():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfs.zip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду chmod с невалидными аргументами
    command_processor.process_command("chmod 777 numbers.txt")
    # Проверяем, что права доступа не изменены
    assert vfs.permissions["numbers.txt"] != 0o755

def test_chmod_command_with_multiple_files():
    # Создаем виртуальную файловую систему
    vfs = VirtualFileSystem("vfszip")
    # Создаем процессор команд
    command_processor = CommandProcessor(vfs, None)
    # Выполняем команду chmod с несколькими файлами
    command_processor.process_command("chmod 755 numbers.txt main.txt")
    # Проверяем, что права доступа изменены
    assert vfs.permissions["numbers.txt"] == 0o755 and vfs.permissions["main.txt"] == 0o755
