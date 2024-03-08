import pymysql

import pymysql
from datetime import datetime
# 只能连接到mysql不能mysql80
# 首先要把mysql服务打开

class mysql_rank:
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
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS ranks(user_id INT NOT NULL ,rank_id INT PRIMARY key NOT NULL,moves INT NOT NULL,create_time date )')

    def insert_ranks(self,number,user_id,moves):
        # 插入数据
        current_time = datetime.now()
        self.sqlQuery = " INSERT INTO ranks (user_id, rank_id, moves, create_time) VALUE (%s,%s,%s,%s) "
        self.value = (user_id,number+1,moves,current_time)
        # print(number)
        try:
            self.cur.execute(self.sqlQuery, self.value)
            self.db.commit()
            print('数据插入成功！')
        except pymysql.Error as e:
            print("数据插入失败：" + e)
            self.db.rollback()

    def users_search(self):
        self.cur.execute("SELECT moves FROM ranks")
        self.results=self.cur.fetchall()
        # print(self.results)

    def search_highest_ranks(self):
        self.cur.execute("SELECT user_name,moves FROM users RIGHT OUTER JOIN ranks ON users.user_id=ranks.user_id ORDER BY moves LIMIT 5;")
        self.highest_results=self.cur.fetchall()