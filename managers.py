import argparse
import sys

from commands import AddRecordCommand, ShowBalanceCommand, FilterRecordCommand


class CommandManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser("Base", add_help=False)
        self.command_list = {
            "add_record": AddRecordCommand,
            "show_balance": ShowBalanceCommand,
            "filter_record": FilterRecordCommand,
        }
        self.parser.add_argument(
            "command", metavar="command", choices=self.command_list.keys()
        )

    def execute(self):
        command = self.parser.parse_known_args()[0].command
        # TODO sys.stdout in command classes
        command_execution_result = self.command_list[command](self.parser)()
        # Print command execution result
        sys.stdout.write(str(command_execution_result))
        sys.stdout.write("\n")