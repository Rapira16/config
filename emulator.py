import os
import zipfile
import yaml
import xml.etree.ElementTree as ET
import unittest
import stat

class VirtualFileSystem:
    def __init__(self, archive_file):
        self.archive_file = archive_file
        self.zip_ref = zipfile.ZipFile(archive_file, "a")

    def get_file_contents(self, file_path):
        with self.zip_ref.open(file_path, "r") as f:
            return f.read()

    def list_files(self, dir_path):
        files = []
        dirs = []
        for f in self.zip_ref.infolist():
            if f.filename.endswith("/"):  # filter directories
                if dir_path == ".":
                    if f.filename.count("/") == 1:  # only consider top-level directories
                        dirs.append(f.filename[:-1])  # remove trailing slash
                else:
                    if f.filename.startswith(dir_path + "/") and f.filename.count("/") == len(dir_path.split("/")) + 1:
                        dirs.append(f.filename[len(dir_path) + 1:-1])  # remove trailing slash
            else:
                if dir_path == ".":
                    if not "/" in f.filename:
                        files.append(f.filename)
                else:
                    if f.filename.startswith(dir_path + "/"):
                        files.append(f.filename[len(dir_path) + 1:])
        return files, dirs

    def create_dir(self, dir_path):
        if not dir_path.endswith("/"):
            dir_path += "/"
        info = zipfile.ZipInfo(dir_path)
        info.external_attr = 0o755 << 16  # set permissions to 755
        self.zip_ref.writestr(info, "")  # create the directory

    def change_permissions(self, file_path, permissions):
        # Not implemented, as permissions are not applicable to files within a zip archive
        pass

class CommandProcessor:
    def __init__(self, vfs):
        self.vfs = vfs
        self.current_dir = "."

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
        dir_path = args[0] if args else self.current_dir
        files, dirs = self.vfs.list_files(dir_path)
        for file in files:
            print(file)
        for dir in dirs:
            print(dir)  # add trailing slash to indicate directory

    def cd(self, args):
        dir_path = args[0] if args else "."
        if dir_path == "..":
            self.current_dir = self.join_paths(self.current_dir, "..")
        else:
            self.current_dir = self.join_paths(self.current_dir, dir_path)
        print(f"Changed directory to {self.current_dir}")

    def join_paths(self, path1, path2):
        if path1 == ".":
            return path2
        elif path2 == "..":
            return self.join_paths("/".join(path1.split("/")[:-1]), "")
        elif path2 == ".":
            return path1
        else:
            return "/".join([path1, path2]).replace("//", "/")

    def exit(self):
        print("Exiting emulator")
        exit()

    def find(self, args):
        pattern = args[0]
        for f in self.vfs.zip_ref.infolist():
            if pattern in f.filename:
                print(f.filename)

    def mkdir(self, args):
        dir_path = args[0]
        if not dir_path.startswith("/"):
            dir_path = self.join_paths(self.current_dir, dir_path)
        self.vfs.create_dir(dir_path)
        print(f"Directory {dir_path} created")

    def chmod(self, args):
        # Not implemented, as permissions are not applicable to files within a zip archive
        pass

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
        self.command_processor.run_start_script(self.start_script)
        while True:
            user_input = input(f"{self.config['username']}@{self.config['computer_name']} $ ")
            self.command_processor.process_command(user_input)

    def log_action(self, user, action):
        root = ET.Element("log")
        ET.SubElement(root, "action", user=user, action=action)
        tree = ET.ElementTree(root)
        tree.write(self.log_file)

if __name__ == "__main__":
    emulator = Emulator("config.yaml")
    emulator.run()
