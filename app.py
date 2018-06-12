#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app
"""
from flask import Flask, request, redirect, make_response, send_from_directory
from flask import render_template
import datetime
import pandas as pd

TOKEN_KEY = "fk"
TOKEN_STRING = "bbsing"
USERNAME = 'zuturn'
PASSWORD = 'wodemingzi'
EXPORT_CODE = 'thebeast'

app = Flask(__name__)


@app.before_request
def check_login():
    if request.cookies.get(TOKEN_KEY) != TOKEN_STRING:
        if not request.path.startswith('/static') and \
           request.endpoint != 'login':
            return redirect('/login')


@app.route('/')
def index():
    return render_template('index.html', title='dashboard')


@app.route('/export', methods=['GET', 'POST'])
def export_excel():
    alert = False
    data_time=datetime.datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        export_code = request.form.get('exportCode')
        if export_code == EXPORT_CODE:
            return send_from_directory('./stock',filename='data_table.csv',as_attachment=True)
        else:
            alert = True
    return render_template('export.html', title='export', alert=alert, data_time=data_time)


@app.route('/tables', methods=['GET'])
def tables():
    table_data = pd.read_csv('./stock/data_table.csv')
    return render_template('tables.html', title='tables', columns= table_data.columns.tolist(), data=table_data.values.tolist())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            res = make_response(redirect('/'))
            res.set_cookie(TOKEN_KEY, TOKEN_STRING)
            return res
    return render_template('login.html', login=True)


if __name__ == '__main__':
    app.debug = True
    app.run()
