"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 31/03/2018
 Time: 05:12

"""
import sqlite3
import time, datetime


class dbhelper:
    def __init__(self) -> None:
        super().__init__()
        self.table_name = 'tracking_0000_00_00_00_00_00'

    def connect(self):
        """
        connect to database
        :return:
        """
        self.connect = sqlite3.connect('tracking.db')

    def genTableName(self):
        """
        Generate current tablename
        :return:
        """
        today = datetime.datetime.now()
        year = str(today.year)
        month = str(today.month)
        day = str(today.day)
        hour = str(today.hour)
        minutes = str(today.minute)
        seconds = str(today.second)
        self.table_name = 'tracking_' + year + '_' + month + '_' + day + '_' + hour + '_' + minutes + '_' + seconds

    def createTable(self):
        """
        create new table in database
        :return:
        """
        c = self.connect.cursor()
        c.execute('''CREATE TABLE if not exists ''' + self.table_name + '''
             (time time, content text)''')
        self.connect.commit()

    def insertItem(self):
        """
        insert one row in table
        :return:
        """
        self.genTableName()
        self.createTable()
        c = self.connect.cursor()
        c.execute('''
        INSERT INTO ''' + self.table_name + ''' VALUES (?,?)
        ''', [time.time(), 'test text'])
        self.connect.commit()

    def clearDb(self):
        """
        delete all tables
        :return:
        """
        c = self.connect.cursor()
        c.execute('''
            SELECT name FROM sqlite_master WHERE type='table';
        ''')
        row = c.fetchone()
        tables = []
        while row:
            tables.append(row[0])
            row = c.fetchone()
        for table in tables:
            c.execute('DROP TABLE IF EXISTS ' + table)
