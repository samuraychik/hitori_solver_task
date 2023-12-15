class Command:
    def do(self):
        raise NotImplementedError()

    def undo(self):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()


class CommandManager:
    def __init__(self) -> None:
        self.history = list()
        self.trash = list()

    def do(self, command: Command) -> None:
        self.history.append(command)
        self.trash = list()
        command.do()

    def undo(self) -> None:
        try:
            command = self.history.pop()
            command.undo()
            self.trash.append(command)
        except IndexError:
            print("<ERROR> History is empty")

    def redo(self) -> None:
        try:
            command = self.trash.pop()
            command.do()
            self.history.append(command)
        except IndexError:
            print("<ERROR> Trash is empty")
