"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 31/03/2018
 Time: 05:12

"""
import random
import sqlite3
import string
import time, datetime
import os


class dbhelper:
    def __init__(self) -> None:
        super().__init__()
        self.view_file_path = './sql/create_view.sql'
        self.table_name = 'tracking_0000_00_00_00_00_00'

    def connect(self):
        """
        connect to database
        :return:
        """
        self.connect = sqlite3.connect('tracking.db')

    def dropView(self, name):
        c = self.connect.cursor()
        c.execute("drop view if exists " + name)

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
        size = random.randint(16, 255)
        chars = string.ascii_uppercase + string.digits
        content = ''.join(random.choice(chars) for _ in range(size))
        c.execute('''
        INSERT INTO ''' + self.table_name + ''' VALUES (?,?)
        ''', [
            time.time(),
            content
        ])
        self.connect.commit()

    def getTables(self):
        """
        Получаем все таблицы в БД
        :return:
        """
        c = self.connect.cursor()
        c.execute('''
            SELECT name FROM sqlite_master WHERE type='table' and name like '%tracking%';
        ''')
        row = c.fetchone()
        tables = []
        while row:
            tables.append(row[0])
            row = c.fetchone()
        return tables

    def createView(self):
        """
        Создаем главное представление, содержащее все данные
        :return:
        """
        c = self.connect.cursor()
        views = self.createInnerJoin()
        self.dropView('tracking')
        sql_create_views = " create view tracking as "
        views = list(map(lambda view_name: "\n select * from " + view_name, views))
        sql_create_views += "\n union all ".join(views)
        f = open(self.view_file_path, 'a')
        f.write(sql_create_views)
        f.close()
        c.execute(sql_create_views)
        self.connect.commit()
        current_time = time.time()
        self.createSelect(current_time - 7, current_time - 4)

    def createInnerJoin(self):
        """
        Создаем внутренние джойны низкой размерности
        Для SQLite не удалось создать view из более чем 500 таблиц
        :return:
        """
        c = self.connect.cursor()
        count_inner_views = 1
        views = []
        self.dropView('tracking_' + str(count_inner_views))
        sql = " create view tracking_" + str(count_inner_views) + " as "
        views.append('tracking_' + str(count_inner_views))
        if os.path.isfile(self.view_file_path):
            os.remove(self.view_file_path)
        tables = self.getTables()
        f = True
        i = 0
        select_from_tables = list(map(lambda table_name: "\n select * from " + table_name, tables))
        for table in select_from_tables:
            if not f:
                sql += """\nunion all """
            sql += " " + table
            f = False
            if (i > 1) and ((i % 450) == 0):
                c.execute(sql)
                f = open(self.view_file_path, 'a')
                f.write(sql)
                f.close()
                count_inner_views += 1
                self.dropView('tracking_' + str(count_inner_views))
                sql = " create view tracking_" + str(count_inner_views) + " as "
                views.append('tracking_' + str(count_inner_views))
                f = True
            i += 1
        f = open(self.view_file_path, 'a')
        f.write(sql)
        f.close()
        c.execute(sql)
        return views

    def createSelect(self, time_start, time_end):
        """
        Создаем селект для выборки данных в промежутке от time_start до time_end
        :return:
        """
        if os.path.isfile('./sql/select.sql'):
            os.remove('./sql/select.sql')
        datetime_start = datetime.datetime.fromtimestamp(time_start)
        datetime_end = datetime.datetime.fromtimestamp(time_end)

        year_start = str(datetime_start.year)
        month_start = str(datetime_start.month)
        day_start = str(datetime_start.day)
        hour_start = str(datetime_start.hour)
        minutes_start = str(datetime_start.minute)
        seconds_start = str(datetime_start.second)

        year_end = str(datetime_end.year)
        month_end = str(datetime_end.month)
        day_end = str(datetime_end.day)
        hour_end = str(datetime_end.hour)
        minutes_end = str(datetime_end.minute)
        seconds_end = str(datetime_end.second)
        # Определяем срез таблиц, в котором будем искать данные
        table_search_name_start = 'tracking_' + year_start + '_' + month_start + '_' + day_start + '_' + hour_start + '_' + minutes_start + '_' + seconds_start
        table_search_name_end = 'tracking_' + year_end + '_' + month_end + '_' + day_end + '_' + hour_end + '_' + minutes_end + '_' + seconds_end

        sql = """
        select name from sqlite_master 
        where  
            type = 'table'
            and name >= '""" + table_search_name_start + """"'
            and name <= '""" + table_search_name_end + """"'
        """
        c = self.connect.cursor()
        c.execute(sql)
        row = c.fetchone()
        tables = []
        while row:
            tables.append(row[0])
            row = c.fetchone()
        if not len(tables):
            return
        tables = list(map(lambda table_name: "\n select * from " + table_name, tables))
        sql = """ select * from ( """
        sql += "\n union all ".join(tables)
        sql += """)
                where 
                time >= """ + str(time_start) + """
                 and time <= """ + str(time_end)
        f = open('./sql/select.sql', 'w')
        f.write(sql)
        f.close()

    def clearDb(self):
        """
        delete all tables
        :return:
        """
        c = self.connect.cursor()
        tables = self.getTables()
        for table in tables:
            c.execute('DROP TABLE IF EXISTS ' + table)

        self.connect.commit()
