import tkinter
import pygame
import threading
import os,sys,time
import platform
import hashlib
from mysql_users import mysql_users
from tkinter import messagebox
#这里有两个问题，一个是怎么多线程，一个是怎么把tkinter窗口嵌入
class Login:
    def __init__(self,stats):
        self.users = mysql_users()
        self.root = tkinter.Tk()
        self.root.geometry('800x500')
        self.root.title('欢迎使用登录注册页面')
        #这里显示背景图片
        self.label=tkinter.Label(self.root)
        self.background_img=tkinter.PhotoImage(file='images/login_back.png')
        self.label.config(image=self.background_img)
        self.label.pack()
        self.password_sent = ''
        self.username_sent = ''
        self.labelname = tkinter.Label(self.root, text='用户名', justify=tkinter.RIGHT, width=80)
        self.labelname.place(x=300, y=200, width=80, height=20)
        # stringvar创建一个可变的字符串
        self.varname = tkinter.StringVar(self.root, value='')
        # 输入文本框
        self.entryname = tkinter.Entry(self.root, width=80, textvariable=self.varname)
        self.entryname.place(x=370, y=200, width=80, height=20)

        self.labelpwd = tkinter.Label(self.root, text='密码', justify=tkinter.RIGHT, width=80)
        self.labelpwd.place(x=300, y=250, width=80, height=20)
        self.varpwd = tkinter.StringVar(self.root, value='')
        # 输入文本框
        self.entrypwd = tkinter.Entry(self.root, show='*', width=80, textvariable=self.varpwd)
        self.entrypwd.place(x=370, y=250, width=80, height=20)

        self.button_login = tkinter.Button(self.root, text='登录', command=self.login)
        # 这里的login事件
        self.button_login.place(x=300, y=300, width=50, height=20)

        self.button_signup = tkinter.Button(self.root, text='注册', command=self.signup)
        # 这里的signup事件
        self.button_signup.place(x=400, y=300, width=50, height=20)

        self.stats=stats
        # print(id(self.stats.game_stats))
        # print(id(stats.game_stats))
        self.login_success = 0




    def login(self):
        self.name_login = self.entryname.get()
        self.pwd_login = self.entrypwd.get()
        self.users.users_search()
        self.users_info=self.users.results
        name_list=[ i[1] for i in self.users_info]
        #对密码进行处理
        password_encoded = self.pwd_login.encode()
        password_hash = hashlib.md5()
        password_hash.update(password_encoded)
        # 判断用户名或密码不能为空
        if not (self.name_login and self.pwd_login):
            tkinter.messagebox.showwarning(title='警告', message='用户名或密码不能为空')
        # 判断用户名和密码是否匹配
        elif self.name_login in name_list:
            if password_hash.hexdigest() == self.users_info[name_list.index(self.name_login)][2]:
                #messagebox对话框会以modal的方式显示，也就是会阻塞程序的执行，直到被关闭为止
                self.id=self.users_info[name_list.index(self.name_login)][0]
                # print('self.id')
                # print(self.id)

                tkinter.messagebox.showinfo(title='欢迎您', message='       登录成功！\r\n当前登录账号为：' + self.name_login)
                self.login_over()
            else:
                tkinter.messagebox.showerror(title='错误', message='密码输入错误')
        # 账号不在数据库中，则弹出是否注册的框
        else:
            tkinter.messagebox.askyesno(title='提示', message='该账号不存在，请点击注册')


    def login_over(self):
        # print(self.name_login)
        # print(self.pwd_login)
        self.stats.game_stats = 1
        self.login_success=1
        # print(self.stats.game_stats)
        self.root.destroy()
        self.root.quit()
        self.users.db.close()
        self.users.cur.close()

    def signup(self):
        self.name_signup = self.entryname.get()
        self.pwd_signup = self.entrypwd.get()
        self.users.users_search()
        self.users_info = self.users.results
        name_list = [i[1] for i in self.users_info]
        self.number=len(self.users_info)
        self.id = self.number+1
        print('self.id')
        print(self.id)
        # 判断用户名或密码不能为空
        if not (self.name_signup and self.pwd_signup):
            tkinter.messagebox.showwarning(title='警告', message='用户名或密码不能为空')

        elif self.name_signup not in name_list:
            tkinter.messagebox.showinfo(title='欢迎您', message='       注册成功！\r\n当前登录账号为：' + self.name_signup)
            self.signup_over()
        else:
            tkinter.messagebox.askyesno(title='提示', message='该账号已注册')
        # print(self.name_signup)
        # print(self.pwd_signup)

    def signup_over(self):

        self.users.signup_mysql(self.number,self.name_signup,self.pwd_signup)
        self.stats.game_stats = 1
        self.login_success=1
        self.root.destroy()
        self.root.quit()
        self.users.db.close()
        self.users.cur.close()





if __name__ == '__main__':
    login1 = Login()
    login1.root.mainloop()




