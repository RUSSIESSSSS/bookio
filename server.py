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
    db = Connect(host='127.0.0.1', port=3306, database='book', user='root', password='Zxcvbnm,123456', charset='utf8')
    return db


@app.route('/index')
def index():
    return render_template('index.html')


# 新增book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        book_name = request.values.get('book_name')
        book_price = request.values.get('book_price')
        book_summary = request.values.get('book_summary')
        db = get_db()
        cursor = db.cursor()
        sql = 'INSERT INTO book (book_name, book_price, book_summary) VALUES (%s,%s,%s);'
        cursor.execute(query=sql, args=[book_name, book_price, book_summary])
        db.commit()
        cursor.close()
        return redirect('/index')  # 添加完成之后返回到/index页


# 查询所有book后需要返回到数据列表页
@app.route('/getbooks', methods=['GET'])
def get_books():
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        sql = 'select * from book;'
        cursor.execute(query=sql)
        books = cursor.fetchall()
        data = []
        for book in books:
            b = {}
            b['book_id'] = book[0]
            b['book_name'] = book[1]
            b['book_price'] = book[2]
            b['book_summary'] = book[3]
            data.append(b)
        cursor.close()
        return jsonify(data)


# 修改book信息
@app.route('/updatebook/<book_id>', methods=['GET', 'POST'])
def change_std(book_id):
    if request.method == 'GET':
        return render_template("update.html")
    else:
        jsondata = request.json
        print("啊啊啊啊啊啊啊啊啊啊啊啊", type(jsondata))

        # jsondata = request.values
        book_name = jsondata.get('book_name')
        book_price = jsondata.get('book_price')
        book_summary = jsondata.get('book_summary')
        db = get_db()
        cursor = db.cursor()
        sql = f'update book set book_name=%s, book_price=%s, book_summary=%s where book_id = {book_id}  ;'
        cursor.execute(query=sql, args=[book_name, book_price, book_summary])
        db.commit()
        cursor.close()
        return redirect('/getbooks')


@app.route('/deletebook/<book_id>', methods=['GET', 'POST'])
def delete_book_by_book_id(book_id):
    if request.method == 'GET':
        return render_template('update.html')
    else:
        db = get_db()
        cursor = db.cursor()
        sql = f'delete from book where book_id = {book_id}'
        cursor.execute(query=sql)
        db.commit()
        cursor.close()
        return redirect('/getbooks')


# 删除某本book

if __name__ == '__main__':
    app.run(debug=True)
