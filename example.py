"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 31/03/2018
 Time: 05:14

"""
import time

from dbhelper import dbhelper

db = dbhelper()
db.connect()
# db.createView()
time_start = time.time()
c = db.connect.cursor()
c.execute("""
 select * from ( 
 select * from tracking_2018_4_1_8_48_7
 union all 
 select * from tracking_2018_4_1_8_48_8
 union all 
 select * from tracking_2018_4_1_8_48_9)
                where 
                time >= 1522561686.1784
                 and time <= 1522561689.1784
                 """)
time_end = time.time()
time_exec = time_end - time_start
print("Время выполнения запроса к partition ? секунд.", time_exec)

time_start = time.time()
c.execute("""
select * from tracking 
                where 
                time >= 1522561686.1784
                 and time <= 1522561689.1784
""")
time_end = time.time()
time_exec = time_end - time_start
print("Время выполнения запроса к view ? секунд.", time_exec)
