import pandas as pd


class Wear:
    def __init__(self, name_file):
        self.name_file = name_file
        self.data = ''

    def read_xlsx(self):
        self.data = pd.read_excel(self.name_file)
        self.data.head()


def main():
    w = Wear('Resources/__Интенсивность износа с уклонами .xlsx')
    w.read_xlsx()


main()