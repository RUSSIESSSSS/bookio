#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : paulinelee
# @Time     : 2024/6/4 14:06
# @File     : server.py
# @Project  : flask_book


from flask import Flask, render_template, request, redirect, jsonify
from pymysql import Connect

app = Flask(__name__)


def get_db():
    db = Connect(host='127.0.0.1', port=3306, database='book', user='root', password='123456', charset='utf8')
    return db


@app.route('/index')
def index():
    return render_template('index.html')  # 吧一个页面返回给前端


# 新增book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        json_data = request.form  # 返回一个字典
        book_name = json_data.get('book_name')
        book_price = json_data.get('book_price')
        book_summary = json_data.get('book_summary')
        book_quantity = json_data.get('book_quantity')
        db = get_db()
        cursor = db.cursor()
        sql = 'INSERT INTO book (book_name, book_price, book_summary,book_quantity) VALUES (%s,%s,%s,%s);'
        cursor.execute(query=sql, args=[book_name, book_price, book_summary, book_quantity])
        db.commit()
        cursor.close()
        return redirect('/index')  # 添加完成之后返回到/index页
        # return json_data   #返回请求的数据


# 查询所有book后需要返回到数据列表页
@app.route('/getbooks', methods=['GET', 'POST'])
def get_books():
    if request.method == 'GET':
        return render_template('getbooks.html')
    else:
        db = get_db()
        cursor = db.cursor()
        sql = 'select * from book;'
        cursor.execute(query=sql)
        books = cursor.fetchall()  # 返回一个元组
        data = []
        for book in books:
            b = {}
            b['book_id'] = book[0]
            b['book_name'] = book[1]
            b['book_price'] = book[2]
            b['book_summary'] = book[3]
            data.append(b)
        cursor.close()
        return data


# 修改book信息
@app.route('/updatebook/<int:book_id>', methods=['GET', 'POST'])  # bookid是公开路由
def update_book(book_id):
    if request.method == 'GET':
        return render_template("update.html")
    else:
        jsondata = request.form
        book_name = jsondata.get('book_name')
        book_price = jsondata.get('book_price')
        book_summary = jsondata.get('book_summary')
        book_quantity = jsondata.get('book_quantity')
        db = get_db()
        cursor = db.cursor()
        sql = f'''update book set book_name=%s, book_price=%s, book_summary=%s, book_quantity=%s where book_id  ={book_id};'''  # tmd这个sql总是报错
        cursor.execute(query=sql, args=[book_name, book_price, book_summary, book_quantity])
        db.commit()
        cursor.close()
        return jsondata


@app.route('/deletebook/<int:book_id>')
def delete_book_by_book_id(book_id):
    db = get_db()
    cursor = db.cursor()
    sql = f'''delete from book where book_id ={book_id};'''
    cursor.execute(query=sql)
    db.commit()
    cursor.close()
    return redirect('/getbooks')


@app.route('/search', methods=['GET'])
def search():
    """通过book_name 和book_summary进行搜索"""
    key = request.args.get('key')
    db = get_db()
    cursor = db.cursor()
    sql = 'select * from book where book_name like %s or book_summary like %s;'
    cursor.execute(sql, ['%' + key + '%', '%' + key + '%'])
    res = cursor.fetchall()

    l = []
    for i in res:
        b = {}
        b['book_name'] = i[0]
        b['book_price'] = i[1]
        b['book_summary'] = i[2]
        b['book_quantity'] = i[3]
        l.append(b)
    cursor.close()
    return l


# 删除某本book

if __name__ == '__main__':
    app.run(port=8888, host='0.0.0.0', debug=True)
