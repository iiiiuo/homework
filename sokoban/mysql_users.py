import pymysql

import pymysql
import hashlib
from datetime import datetime
#只能连接到mysql不能mysql80
#首先要把mysql服务打开

class mysql_users:
    def __init__(self):
        DBHOST = 'localhost'
        DBUSER = 'root'
        DBPASS = 'root'
        DBNAME = 'users'
        try:
            self.db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
            print('数据库连接成功!')
        except pymysql.Error as e:
            print('数据库连接失败' + str(e))
            #创建游标对象
        self.cur = self.db.cursor()
        self.cur.execute('CREATE DATABASE IF NOT EXISTS users')
        self.cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY key NOT NULL ,user_name VARCHAR(20) NOT NULL,user_password VARCHAR(32),register_time date )')

    def signup_mysql(self,number,user_name,user_password):
        #查询表内人数

        current_time=datetime.now()
        #插入数据
        password_encoded = user_password.encode()
        password_hash=hashlib.md5()
        password_hash.update(password_encoded)
        # print(password_hash.hexdigest())
        self.sqlQuery = " INSERT INTO users (user_id, user_name, user_password, register_time) VALUE (%s,%s,%s,%s) "
        self.value = (number+1, user_name, password_hash.hexdigest(), current_time)
        try:
            self.cur.execute(self.sqlQuery, self.value)
            self.db.commit()
            print('数据插入成功！')
        except pymysql.Error as e:
            print("数据插入失败：" + e)
            self.db.rollback()

    def users_search(self):
        self.cur.execute("SELECT user_id, user_name,user_password FROM users")
        self.results=self.cur.fetchall()
        # print(self.results)



