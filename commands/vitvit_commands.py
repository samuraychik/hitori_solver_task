class Command:
    def do(self):
        raise NotImplementedError()

    def undo(self):
        raise NotImplementedError()


class CommandManager:
    def __init__(self) -> None:
        self.history = list()

    def do(self, command: Command) -> None:
        self.history.append(command)
        command.do()

    def undo(self) -> None:
        try:
            command = self.history.pop()
            command.undo()
            del command
        except IndexError:
            print("<CM_ERROR> History is empty")
