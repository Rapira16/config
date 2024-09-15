import zipfile
import yaml
import xml.etree.ElementTree as ET

# Класс виртуальной файловой системы
class VirtualFileSystem:
    def __init__(self, archive_file):
        # Инициализация виртуальной файловой системы
        self.archive_file = archive_file
        self.zip_ref = zipfile.ZipFile(archive_file, "a")
        self.permissions = {}

    # Получение содержимого файла
    def get_file_contents(self, file_path):
        # Открываем файл в режиме чтения
        with self.zip_ref.open(file_path, "r") as f:
            # Возвращаем содержимое файла
            return f.read()

    # Список файлов и директорий
    def list_files(self, dir_path):
        # Инициализируем списки файлов и директорий
        files = []
        dirs = []
        # Перебираем все файлы в архиве
        for f in self.zip_ref.infolist():
            # Если файл является директорией
            if f.filename.endswith("/"):
                # Если директория находится в корне
                if dir_path == ".":
                    # Если директория является верхним уровнем
                    if f.filename.count("/") == 1:
                        # Добавляем директорию в список
                        dirs.append(f.filename[:-1])
                else:
                    # Если директория находится в поддиректории
                    if f.filename.startswith(dir_path + "/") and f.filename.count("/") == len(dir_path.split("/")) + 1:
                        # Добавляем директорию в список
                        dirs.append(f.filename[len(dir_path) + 1:-1])
            else:
                # Если файл не является директорией
                if dir_path == ".":
                    # Если файл находится в корне
                    if not "/" in f.filename:
                        # Добавляем файл в список
                        files.append(f.filename)
                else:
                    # Если файл находится в поддиректории
                    if f.filename.startswith(dir_path + "/"):
                        # Добавляем файл в список
                        files.append(f.filename[len(dir_path) + 1:])
        # Возвращаем списки файлов и директорий
        return files, dirs

    # Создание директории
    def create_dir(self, dir_path):
        # Если директория не заканчивается на слеш
        if not dir_path.endswith("/"):
            # Добавляем слеш в конец директории
            dir_path += "/"
        # Создаем информацию о директории
        info = zipfile.ZipInfo(dir_path)
        # Устанавливаем права доступа 755
        info.external_attr = 0o755 << 16
        # Создаем директорию
        self.zip_ref.writestr(info, "")

    # Изменение прав доступа
    def change_permissions(self, file_path, permissions):
        # Изменяем права доступа файла
        self.permissions[file_path] = permissions

# Класс процессора команд
class CommandProcessor:
    def __init__(self, vfs, emulator):
        # Инициализация процессора команд
        self.vfs = vfs
        self.current_dir = "."
        self.emulator = emulator

    # Запуск стартового скрипта
    def run_start_script(self, script_file):
        # Открываем скрипт в режиме чтения
        with open(script_file, "r") as f:
            # Читаем содержимое скрипта
            script_contents = f.read()
        # Перебираем все команды в скрипте
        for line in script_contents.splitlines():
            # Обрабатываем команду
            self.process_command(line)

    # Обработка команды
    def process_command(self, user_input):
        # Разделяем команду на части
        command, *args = user_input.split()
        # Обрабатываем команду
        if command == "ls":
            self.ls(args)
        elif command == "cd":
            self.cd(args)
        elif command == "exit":
            self.exit()
        elif command == "find":
            self.find(args)
        elif command == "mkdir":
            self.mkdir(args)
        elif command == "chmod":
            self.chmod(args)
        else:
            # Если команда неизвестна
            print("Unknown command")

    # Команда ls
    def ls(self, args):
        # Если директория не указана
        if not args:
            # Используем текущую директорию
            dir_path = self.current_dir
        else:
            # Используем указанную директорию
            dir_path = args[0]
        # Получаем список файлов и директорий
        files, dirs = self.vfs.list_files(dir_path)
        # Выводим список файлов
        for file in files:
            print(file)
        # Выводим список директорий
        for dir in dirs:
            print(dir)

    # Команда cd
    def cd(self, args):
        # Если директория не указана
        if not args:
            # Используем текущую директорию
            dir_path = "."
        else:
            # Используем указанную директорию
            dir_path = args[0]
        # Если директория является родительской
        if dir_path == "..":
            # Переходим в родительскую директорию
            self.current_dir = self.join_paths(self.current_dir, "..")
        else:
            # Переходим в указанную директорию
            self.current_dir = self.join_paths(self.current_dir, dir_path)

    # Объединение путей
    def join_paths(self, path1, path2):
        # Если первый путь является текущей директорией
        if path1 == ".":
            # Возвращаем второй путь
            return path2
        # Если второй путь является родительской директорией
        elif path2 == "..":
            # Переходим в родительскую директорию
            return self.join_paths("/".join(path1.split("/")[:-1]), "")
        # Если второй путь является текущей директорией
        elif path2 == ".":
            # Возвращаем первый путь
            return path1
        else:
            # Объединяем пути
            return "/".join([path1, path2]).replace("//", "/")

    # Команда exit
    def exit(self):
        # Выводим сообщение об выходе
        print("Exiting emulator")
        # Логируем действие
        self.emulator.log_action("exit")
        # Останавливаем эмулятор
        self.emulator.stop()
        # Выходим из программы
        exit()

    # Команда find
    def find(self, args):
        # Получаем шаблон поиска
        pattern = args[0]
        # Перебираем все файлы в архиве
        for f in self.vfs.zip_ref.infolist():
 # Если файл соответствует шаблону
            if pattern in f.filename:
                # Выводим файл
                print(f.filename)

    # Команда mkdir
    def mkdir(self, args):
        # Получаем путь директории
        dir_path = args[0]
        # Если директория не является абсолютной
        if not dir_path.startswith("/"):
            # Добавляем текущую директорию к пути
            dir_path = self.join_paths(self.current_dir, dir_path)
        # Создаем директорию
        self.vfs.create_dir(dir_path)

    # Команда chmod
    def chmod(self, args):
        # Получаем путь файла
        file_path = args[0]
        # Получаем права доступа
        permissions = int(args[1], 8)
        # Изменяем права доступа файла
        self.vfs.change_permissions(file_path, permissions)

# Класс эмулятора
class Emulator:
    def __init__(self, config_file, username, computer_name):
        # Инициализация эмулятора
        self.config = self.load_config(config_file)
        self.config["username"] = username
        self.config["computer_name"] = computer_name
        self.vfs = VirtualFileSystem(self.config["vfs_archive"])
        self.log_file = self.config["log_file"]
        self.start_script = self.config["start_script"]
        self.command_processor = CommandProcessor(self.vfs, self)
        self.actions = []

    # Загрузка конфигурации
    def load_config(self, config_file):
        # Открываем файл конфигурации в режиме чтения
        with open(config_file, "r") as f:
            # Читаем содержимое файла
            return yaml.safe_load(f)

    # Запуск эмулятора
    def run(self):
        # Запускаем стартовый скрипт
        self.command_processor.run_start_script(self.start_script)
        # Входим в цикл обработки команд
        while True:
            # Получаем текущую директорию
            current_dir = self.command_processor.current_dir
            # Если текущая директория является корневой
            if current_dir == ".":
                # Создаем приглашение
                prompt = f"{self.config['username']}@{self.config['computer_name']}~$ "
            else:
                # Создаем приглашение с текущей директорией
                current_dir_levels = current_dir.split("/")
                prompt_levels = [level for level in current_dir_levels]
                prompt = f"{self.config['username']}@{self.config['computer_name']}~/{'/'.join(prompt_levels)}$ "
            # Читаем ввод пользователя
            user_input = input(prompt)
            # Обрабатываем команду
            self.command_processor.process_command(user_input)
            # Логируем действие
            self.log_action(user_input)

    # Логирование действия
    def log_action(self, user_input):
        # Добавляем действие в список
        self.actions.append({"user": self.config["username"], "action": user_input})

    # Остановка эмулятора
    def stop(self):
        # Добавляем действие остановки в список
        self.actions.append({"user": self.config["username"], "action": "exit"})
        # Создаем корневой элемент лога
        root = ET.Element("log")
        # Перебираем все действия
        for action in self.actions:
            # Создаем элемент действия
            ET.SubElement(root, "action", user=action["user"], action=action["action"])
        # Создаем дерево элементов
        tree = ET.ElementTree(root)
        # Записываем лог в файл
        tree.write(self.log_file)

if __name__ == "__main__":
    # Получаем файл конфигурации
    config_file = "config.yaml"
    # Получаем имя пользователя
    username = input("Enter username: ")
    # Получаем имя компьютера
    computer_name = input("Enter computer name: ")
    # Создаем эмулятор
    emulator = Emulator(config_file, username, computer_name)
    # Запускаем эмулятор
    try:
        emulator.run()
    except KeyboardInterrupt:
        # Останавливаем эмулятор при прерывании
        emulator.stop()