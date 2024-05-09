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
        self.parser = argparse.ArgumentParser(
            "Personal financial management CLI application", add_help=False
        )
        self.parser.add_argument(
            "command",
            metavar="command",
            help=f"Action to be executed, current choices are {','.join(self.command_list)}",
            choices=self.command_list.keys(),
        )

    def execute(self, *args, **kwargs):
        command = self.parser.parse_known_args(*args, **kwargs)[0].command
        try:
            self.command_list[command](self.parser)(*args, **kwargs)
        except ValueError as exc:
            # handle possible exceptions and output error message for user
            self.parser.error(exc.args[0])
