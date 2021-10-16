from flask import render_template , request , Markup , url_for , redirect , session, sessions,send_file
import os
from HR_Recruiting_Staff import app
# from datetime import datetime, timedelta
from flask_ckeditor import CKEditor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
import sqlite3
from sqlalchemy import create_engine
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import pymysql.cursors
from HR_Recruiting_Staff.thu_vien.xu_ly_form import *
from HR_Recruiting_Staff.thu_vien.xu_ly_3L import *
# from GGG.thu_vien.connection import *
import socket  
from HR_Recruiting_Staff.thu_vien.connection import *
import datetime

upload_folder = app.static_folder
app.config['UPLOAD_FOLDER'] = upload_folder
from io import BytesIO

import sqlite3
import openpyxl



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'linhnhi1198@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qq@1234567'
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)






Dangnhapthatbai = ""
# =========================================Start TRANG CHỦ==============================================
# =========================================Start TRANG CHỦ==============================================
@app.route("/", methods=["GET", "POST"])
def index():
    chuoi_html_index_brand = CHUOI_HTML_INDEX_BRAND()

    return render_template('index.html', CHUOI_HTML_HIEN_THI_INDEX_BRAND = chuoi_html_index_brand)
# =========================================END TRANG CHỦ=====================================================
# ======================END TRANG CHỦ=



# ===========================ĐĂNG Xuat Start=====================================
# ===========================ĐĂNG Xuat Start=====================================
@app.route('/dang-xuat', methods=['GET', 'POST'])
def dang_xuat():
    session.pop('session_username', None)
    session.pop('session_quyen', None)
    session.pop('session_phong_ban', None)
    session.pop('session_manv', None)
    return redirect(url_for('index'))
    # return render_template('login.html',USER = user1 , PASS = pass1)
# ===========================ĐĂNG Xuat END=====================================
# ===========ĐĂNG Xuat END===================



@app.route("/<string:ma_brand>", methods = ["POST","GET"])
def brand(ma_brand):
    
    ok = test
    if request.form.get('user_dang_nhap'):
        print(request.form.get('user_dang_nhap'))
    return render_template('chi_tiet_ban_tin.html')