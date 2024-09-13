import os
import zipfile
import yaml
import xml.etree.ElementTree as ET
import unittest
import stat

class VirtualFileSystem:
    def __init__( self, archive_file):
        self.archive_file = archive_file
        self.extracted_files = {}

    def extract_archive(self):
        with zipfile.ZipFile(self.archive_file, "r") as zip_ref:
            zip_ref.extractall()

    def get_file_contents(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    def list_files(self, dir_path):
        return os.listdir(dir_path)

    def create_dir(self, dir_path):
        os.mkdir(dir_path)

    def change_permissions(self, file_path, permissions):
        os.chmod(file_path, permissions)

class CommandProcessor:
    def __init__(self, vfs):
        self.vfs = vfs

    def run_start_script(self, script_file):
        with open(script_file, "r") as f:
            script_contents = f.read()
        for line in script_contents.splitlines():
            self.process_command(line)

    def process_command(self, user_input):
        print(user_input)
        command, *args = user_input.split()
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
            print("Unknown command")

    def ls(self, args):
        dir_path = args[0] if args else "."
        files = self.vfs.list_files(dir_path)
        for file in files:
            print(file)

    def cd(self, args):
        dir_path = args[0] if args else "."
        os.chdir(dir_path)

    def exit(self):
        print("Exiting emulator")
        exit()

    def find(self, args):
        pattern = args[0]
        for root, dirs, files in os.walk("."):
            for file in files:
                if pattern in file:
                    print(os.path.join(root, file))

    def mkdir(self, args):
        dir_path = args[0]
        self.vfs.create_dir(dir_path)

    def chmod(self, args):
        file_path = args[0]
        permissions = int(args[1], 8)
        self.vfs.change_permissions(file_path, permissions)

class Emulator:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.vfs = VirtualFileSystem(self.config["vfs_archive"])
        self.log_file = self.config["log_file"]
        self.start_script = self.config["start_script"]
        self.command_processor = CommandProcessor(self.vfs)

    def load_config(self, config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)

    def run(self):
        self.vfs.extract_archive()
        self.command_processor.run_start_script(self.start_script)
        while True:
            user_input = input(f"{self.config['username']}@{self.config['computer_name']} $ ")
            self.command_processor.process_command(user_input)

    def log_action(self, user, action):
        root = ET.Element("log")
        ET.SubElement(root, "action", user=user, action=action)
        tree = ET.ElementTree(root)
        tree.write(self.log_file)

def test_ls():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("ls")
    assert vfs.list_files(".") == ["file1", "file2"]

def test_cd():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("cd dir1")
    assert os.getcwd() == "dir1"

def test_exit():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("exit")
    assert emulator.running == False

def test_find():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("find file1")
    assert vfs.get_file_contents("file1") == " contents "

def test_mkdir():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("mkdir dir2")
    assert os.path.exists("dir2")

def test_chmod():
    emulator = Emulator("config.yaml")
    vfs = VirtualFileSystem("vfs.zip")
    command_processor = CommandProcessor(vfs)
    command_processor.process_command("chmod 755 file1")
    assert stat.S_IMODE(os.stat("file1").st_mode) == 0o755

if __name__ == "__main__":
    emulator = Emulator("config.yaml")
    emulator.run()
    unittest.main()