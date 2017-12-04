class File:
    def __init__(self, filename):
        self.filename = filename

        with open(self.filename) as fl:
            self.content = fl.read()

        self.lines = tuple(self.content.splitlines(True))

# TODO A File is considered to be equal if the contents are the same.
# TODO this check can be sped up by comparing timestamps.
