import argparse

from commands.commands import (
    AddRecordCommand,
    ShowBalanceCommand,
    FilterRecordCommand,
    EditRecordCommand,
)


class CommandManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser("Base", add_help=False)
        self.command_list = {
            "add_record": AddRecordCommand,
            "edit_record": EditRecordCommand,
            "show_balance": ShowBalanceCommand,
            "filter_record": FilterRecordCommand,
        }
        self.parser.add_argument(
            "command", metavar="command", choices=self.command_list.keys()
        )

    def execute(self):
        command = self.parser.parse_known_args()[0].command
        self.command_list[command](self.parser)()
