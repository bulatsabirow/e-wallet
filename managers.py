import argparse
from commands import AddRecordCommand


class CommandManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser("Base")
        self.command_list = {
            "add_record": AddRecordCommand,
        }
        self.parser.add_argument(
            "command", metavar="command", choices=self.command_list.keys()
        )

    def execute(self):
        command = self.parser.parse_known_args()[0].command
        self.command_list[command](self.parser)()
