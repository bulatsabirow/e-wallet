import argparse

from commands.commands import (
    AddRecordCommand,
    ShowBalanceCommand,
    FilterRecordCommand,
    EditRecordCommand,
)


class CommandManager:
    command_list = {
        "add_record": AddRecordCommand,
        "edit_record": EditRecordCommand,
        "show_balance": ShowBalanceCommand,
        "filter_record": FilterRecordCommand,
    }

    def __init__(self):
        self.parser = argparse.ArgumentParser("Base", add_help=False)
        self.parser.add_argument(
            "command", metavar="command", choices=self.command_list.keys()
        )

    def execute(self, *args, **kwargs):
        command = self.parser.parse_known_args(*args, **kwargs)[0].command
        print("command", command)
        print(self.command_list[command])
        self.command_list[command](self.parser)(*args, **kwargs)
