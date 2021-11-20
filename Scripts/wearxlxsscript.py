import pandas as pd


class WearCalc:
    def __init__(self, name_file):
        self.name_file = name_file
        self.data = ''

    def read_xlsx(self):
        try:
            collection = pd.read_excel(self.name_file, sheet_name=None)
            combined = pd.concat([value.assign(sheet_source=key)
                                  for key, value in collection.items()],
                                  ignore_index=True)
        except:
            print("Ошибка")

def main():
    wear = WearCalc("../Resources/РЦДМ износ.xlsx")
    wear.read_xlsx()


main()