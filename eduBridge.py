# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymysql
import os
import sys
import importlib

importlib.reload(sys)

app = Flask(__name__)

# 全局变量
username = "mirW"
# TODO: username变量的赋值  方法1：全局变量实现，随登录进行修改  方法2：给每个页面传递username
userRole = "CUSTOMER"
notFinishedNum = 0
# 上传文件要储存的目录
UPLOAD_FOLDER = '/static/images/'
# 允许上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
# 首页
def indexpage():
    return render_template('index.html')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('Register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        addr = request.form.get('addr')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )

        if userRole == 'institution':
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from institution where username = '{}' ".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已经存在该机构
            if num == 1:
                print("失败！机构已注册！")
                msg = "fail1"
            else:
                sql2 = "insert into institution (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("机构注册成功")
                    msg = "done1"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail1"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from STUDENT where username = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已存在该学员
            if num == 1:
                print("学员已注册！请直接登录。")
                msg = "fail2"
            else:
                sql2 = "insert into STUDENT (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("学员注册成功")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail2"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)


# 登录
@app.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('logIn.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )

        if userRole == 'ADMIN':
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from ADMIN where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该管理员且密码正确
            if num == 1:
                print("登录成功！欢迎管理员！")
                msg = "done1"
            else:
                print("您没有管理员权限或登录信息出错。")
                msg = "fail1"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'institution':
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from institution where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该机构且密码正确
            if num == 1:
                print("登录成功！欢迎机构学员！")
                msg = "done2"
            else:
                print("您没有机构学员权限或登录信息出错。")
                msg = "fail2"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from STUDENT where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该学员且密码正确
            if num == 1:
                print("登录成功！欢迎学员！")
                msg = "done3"
            else:
                print("您没有学员权限，未注册或登录信息出错。")
                msg = "fail3"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

# 管理员的店铺列表页面
@app.route('/adminRestList', methods=['GET', 'POST'])
def adminRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM institution"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminRestList.html', username=username, messages=msg)
    elif request.form["action"] == "移除":
        RESTName = request.form.get('RESTName')
        # 连接数据库，默认数据库学员名root，密码空
        db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # TODO: 点击移除后显示移除成功，但数据库里没有删掉
        # 删除SERVICE的
        sql1 = "DELETE FROM SERVICE WHERE institution = '{}'".format(RESTName)
        cursor.execute(sql1)
        db.commit()
        # 删除订单表里的
        sql2 = "DELETE FROM ORDER_COMMENT WHERE institution = '{}'".format(RESTName)
        cursor.execute(sql2)
        db.commit()
        # 删除shoppingCart的
        sql3 = "DELETE FROM shoppingCart WHERE institution = '{}'".format(RESTName)
        cursor.execute(sql3)
        db.commit()
        # 删除institution的
        sql4 = "DELETE FROM institution WHERE username = '{}'".format(RESTName)
        cursor.execute(sql4)
        db.commit()
        print(sql4)

        msg = "delete"
        print(msg)

        return render_template('adminRestList.html', username=username, messages=msg)


# 管理员查看评论列表
@app.route('/adminCommentList', methods=['GET', 'POST'])
def adminCommentPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 and text <> ''"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminCommentList.html', username=username, messages=msg)
    elif request.form["action"] == "按评分升序排列":
        db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 AND text is not null Order BY c_rank"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('adminCommentList.html', username=username, messages=msg)

# 学员登录后显示机构列表
@app.route('/UserRestList',methods=['GET', 'POST'])
def UserRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM institution"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('UserRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('UserRestList.html', username=username, messages=msg)

#选择机构进入服务列表
@app.route('/Menu',methods=['GET', 'POST'])
def menu():
    msg = ""
    global institution
    if request.form["action"] == "进入>>":
        institution = request.form['institution']
        print(institution)
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM SERVICE WHERE institution = '%s'" % institution
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('Menu.html', username=username, institution=institution, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, institution=institution, messages=msg)
    elif request.form["action"] == "好课推荐":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM SERVICE WHERE institution = '%s' AND isSpecialty = 1" % institution
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, institution=institution, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, institution=institution, messages=msg)
    elif request.form["action"] == "按销量排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM SERVICE WHERE institution = '%s' Order BY sales DESC" % institution
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, institution=institution, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, institution=institution, messages=msg)
    elif request.form["action"] == "按价格排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM SERVICE WHERE institution = '%s' Order BY price DESC" % institution
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, institution=institution, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, institution=institution, messages=msg)

#查看机构评论
@app.route('/ResComment',methods=['GET','POST'])
def resComment():
    msg = ""
    global institution
    if request.form["action"] == "查看评价":
        institution = request.form['institution']
        print(institution)
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM ORDER_COMMENT WHERE institution = '%s' AND isFinished = 1 AND text <> '' "% institution
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('ResComment.html', username=username, institution=institution, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('ResComment.html', username=username, institution=institution, messages=msg)

#机构查看评论
@app.route('/ResCommentList', methods=['GET', 'POST'])
def ResCommentList():
    msg = ""
    # 连接数据库，默认数据库学员名root，密码空
    institution=username
    print(institution)
    # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='eduDB',
        charset='utf8'
    )
    cursor = db.cursor()
    try:
        cursor.execute("use eduDB")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM ORDER_COMMENT WHERE institution = '%s' AND isFinished = 1 AND text <> '' " % institution
    cursor.execute(sql)
    res = cursor.fetchall()
    # print(res)
    # print(len(res))
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('ResCommentList.html', username=username, institution=institution, result=res,
                                   messages=msg)
    else:
        print("NULL")
        msg = "none"
    return render_template('ResCommentList.html', username=username, institution=institution, messages=msg)

# 购物车
@app.route('/myOrder',methods=['GET', 'POST'])
def shoppingCartPage():
    if request.method == 'GET':
        print("myOrder-->GET")
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('myOrder.html', username=username, messages=msg)
    elif request.form["action"] == "加入购物车":
        print("myOrder-->加入购物车")
        restuarant = request.form['institution']
        servicename = request.form['servicename']
        price = request.form['price']
        img_res = request.form['img_res']
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        sql1 = "insert into SHOPPINGCART  values ('{}','{}','{}','{}','{}') ".format(username,institution,servicename,price,img_res)
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        print(len(res1))
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('myOrder.html', username=username, messages=msg)

    elif request.form["action"] == "结算":
        print("请进行结算")
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        '''
        这下面
        '''
        restuarant = request.form['institution']
        print(institution)
        servicename = request.form['servicename']
        price = request.form['price']
        img_res = request.form['img_res']
        mode = request.form['mode']
        print("==*==")
        print(mode)




# 个人中心页面
@app.route('/personal')
def personalPage():
    return render_template('personal.html')


# 修改个人信息页面
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username)


# 修改密码页面
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库学员名root，密码空
            # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='eduDB',
                charset='utf8'
            )
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username)


@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        print("学员要确认收货啦")
        orderID = request.form['orderID']
        print(orderID)
        sql1 = "Update ORDER_COMMENT SET isFinished = 1, text = '' WHERE orderID = '%s' " % orderID
        print(sql1)
        cursor.execute(sql1)
        db.commit()
        #完成一个订单机构销量加一
        sql2 = "select * from ORDER_COMMENT WHERE orderID = '%s' " % orderID
        cursor.execute(sql2)
        res1 = cursor.fetchone()
        institution = res1[1]
        servicename = res1[2]
        print("{} {} 销量+1".format(servicename, institution))

        sql = "Update SERVICE SET sales = sales+1 WHERE servicename = '{}' AND institution = '{}'" .format(servicename, institution)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        msg = "UpdateSucceed"
        return render_template('OrderPage.html', username=username, messages=msg)

    else:
        return render_template('OrderPage.html', username=username, messages=msg)


@app.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
    msg = ""
    global notFinishedNum

    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成及未评论订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' and isFinished = 1 and text <> '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "待评价订单":
        # 未评价订单跳转到写评论中
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print("MyCommentsPage - 未评价订单: {}".format(len(res)))
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("MyCommentsPage - 待评价订单 - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=len(res))

    else:
        return render_template('MyComments.html', username=username, messages=msg)


@app.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    msg=""
    if request.method == 'GET':
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        # presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        # cursor.execute(presql)
        # res1 = cursor.fetchall()
        # notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - GET - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按交易时间排序":
        # TODO: 排序之后显示的是空的，不显示的问题没有解决
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        print(username)
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - 按交易时间排序 -NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("WriteCommentsPage - 按价格排序 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("WriteCommentsPage - 未完成订单 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('WriteComments.html', username=username, messages=msg)


@app.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "写评论":
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "提交评论":
        print("提交评论!")
        orderID = request.form.get('orderID')
        c_rank = request.form.get('rank')
        text = request.form.get('text')
        db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        sql = "Update ORDER_COMMENT SET text = '{}', c_rank = {} where orderID = '{}'".format(text, c_rank, orderID)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("学员评论成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("学员评论失败")
            msg = "fail"
        return render_template('CommentForm.html', messages = msg, username=username)

#机构查看服务信息
@app.route('/MerchantMenu',methods=['GET', 'POST'])
def MerchantMenu():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM SERVICE WHERE institution = '%s'" % username

        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
    if request.method == 'POST':
        if request.form["action"] == "删除该服务":
            servicename = request.form.get('servicename')
            rest = request.form.get('institution')
            print(rest)
            # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='eduDB',
                charset='utf8'
            )
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "DELETE FROM SERVICE where servicename = '{}' and institution = '{}'".format(servicename,rest)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("菜品删除成功")
                dmsg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品删除失败")
                dmsg = "fail"
            return render_template('MerchantMenu.html', servicename=servicename, rest=rest, dmessages=dmsg)
        elif request.form["action"] == "按销量排序":
            # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='eduDB',
                charset='utf8'
            )
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM SERVICE WHERE institution = '%s' Order BY sales DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html',username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
        elif request.form["action"] == "按价格排序":
            # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='eduDB',
                charset='utf8'
            )
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM SERVICE WHERE institution = '%s' Order BY price DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username,messages=msg)

#机构修改服务信息
@app.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""

    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "修改服务信息":
        servicename = request.form['servicename']#传递过去菜品名
        rest = request.form['institution']#传递过去机构名
        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = request.form.get('isSpecialty')
        #imagesrc = request.form['imagesrc']
        print(servicename)
        print(isSpecialty)
        print(type(isSpecialty))
        
		
        return render_template('MenuModify.html', servicename=servicename, rest=rest, dishinfo=dishinfo, nutriention=nutriention, price=price, username=username, messages=msg,isSpecialty=isSpecialty)
    elif request.form["action"] == "提交修改":

        servicename = request.form.get('servicename')
        rest = request.form.get('rest')

        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        filename = ''
		
        if f !='' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
			
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
		
		
        print(isSpecialty)
        print(type(isSpecialty))
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
			
        if filename == '':
            sql = "Update SERVICE SET dishinfo = '{}', nutriention = '{}', price = {} , isSpecialty = {} where servicename = '{}' and institution = '{}'".format(dishinfo,nutriention,price,isSpecialty,servicename,rest)
        else:
            sql = "Update SERVICE SET dishinfo = '{}', nutriention = '{}', price = {} ,imagesrc = '{}', isSpecialty = {} where servicename = '{}' and institution = '{}'".format(dishinfo,nutriention,price,imgsrc,isSpecialty,servicename,rest)
        print(sql)
		
        try:
            cursor.execute(sql)
            db.commit()
            print("菜品信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("菜品信息修改失败失败")
            msg = "fail"
        return render_template('MenuModify.html',servicename=servicename, rest=rest, username=username, messages=msg)
@app.route('/MenuAdd',methods=['GET','POST'])
def MenuAdd():
    msg = ""
    rest= ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "新增服务":
        rest = request.form['institution']#传递过去机构名
        return render_template('MenuAdd.html',rest=rest)
    elif request.form["action"] == "确认增加":
        servicename = request.form.get('servicename')
        rest = request.form.get('rest')
        dishinfo = request.form.get('dishinfo')
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        f = request.files['imagesrc']
        print(f)
        isSpecialty = int(request.form.get('isSpecialty'))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )

        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from SERVICE where servicename = '{}' ".format(servicename)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # 如果已经存在该机构
        if num == 1:
            print("失败！该菜品已经添加过！")
            msg = "fail1"
        else:
            sql2 = "insert into SERVICE  values ('{}', '{}','{}', '{}',{}, {},'{}', {}) ".format(servicename,rest,dishinfo,nutriention,price,0,imgsrc,isSpecialty)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("菜品添加成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品添加失败")
                msg = "fail"
        return render_template('MenuAdd.html', messages=msg, username=username)



@app.route('/MerchantIndex')

def Merchantindexpage():
    return render_template('MerchantIndex.html')


# 个人中心页面
@app.route('/MerchantPersonal')
def MpersonalPage():
    return render_template('MerchantPersonal.html')


# 修改个人信息页面
@app.route('/MerchantModifyPerInfo', methods=['GET', 'POST'])
def MerchantModifyPerInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPerInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
		
        f = request.files['imagesrc']
        filename = ''
		
        if f !='' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
			
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
		
		
		
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
			
        if filename == '':	
            sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        else:
            sql = "Update {} SET address = '{}', phone = '{}',imageRes = '{}' where username = '{}'".format(userRole, address, phonenum, imgsrc,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)


# 修改密码页面
@app.route('/MerchantModifyPwd', methods=['GET', 'POST'])
def MerModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPwd.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库学员名root，密码空
            # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='eduDB',
                charset='utf8'
            )
            cursor = db.cursor()
            try:
                cursor.execute("use eduDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)

#机构查看订单
@app.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库学员名root，密码空
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE institution = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE institution = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        # db = pymysql.connect("localhost", "root", "123456", "eduDB", charset='utf8')
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='eduDB',
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute("use eduDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)


if __name__ == '__main__':
    app.run(host='localhost', port='8927')
