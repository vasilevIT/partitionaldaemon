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
db.clearDb()
