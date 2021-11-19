import pandas as pd
import pymysql


class Wear:
    def __init__(self, name_file):
        self.name_file = name_file
        self.data = ''

    def read_xlsx(self):
        excel_data = pd.read_excel(self.name_file, sheet_name='351-650')
        print(excel_data.columns.ravel())
        print('Excel Sheet to CSV:n', excel_data.to_csv(index=False))

    def connect_mysql(self):
        con = pymysql.connect('localhost', 'user17',
                              's$cret', 'mydb')
        with con:
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print("Database version: {}".format(version[0]))

    def calculate_wear(self):


def main():
    w = Wear('Resources/РЦДМ износ.xlsx')
    w.read_xlsx()


main()