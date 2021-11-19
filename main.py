import pandas as pd
import pymysql


class Wear:
    def __init__(self, name_file):
        self.name_file = name_file
        self.data = ''

    def read_xlsx(self):
        collection = pd.read_excel(self.name_file, sheet_name=None)

        combined = pd.concat([value.assign(sheet_source=key)
                              for key, value in collection.items()],
                             ignore_index=True)
        pass

    def connect_mysql(self):
        con = pymysql.connect('localhost', 'user17',
                              's$cret', 'mydb')
        with con:
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print("Database version: {}".format(version[0]))

    def calculate_wear(self):
        pass

def main():
    w = Wear('Resources/РЦДМ износ.xlsx')
    w.read_xlsx()


main()