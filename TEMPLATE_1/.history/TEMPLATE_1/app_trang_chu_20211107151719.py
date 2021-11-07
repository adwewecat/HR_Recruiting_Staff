from flask import render_template , request , Markup , url_for , redirect , session, sessions,send_file,jsonify
import os
from TEMPLATE_1 import app
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
from TEMPLATE_1.thu_vien.xu_ly_form import *
from TEMPLATE_1.thu_vien.xu_ly_3L import *
# from GGG.thu_vien.connection import *
import socket  
from TEMPLATE_1.thu_vien.connection import *
import datetime

upload_folder = app.static_folder
app.config['UPLOAD_FOLDER'] = upload_folder
from io import BytesIO

import sqlite3
import openpyxl
# import qrcode


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

    return render_template('index.html', CHUOI_HTML_HIEN_THI_INDEX_BRAND = chuoi_html_index_brand)
# =========================================END TRANG CHỦ=====================================================
# ======================END TRANG CHỦ=



# ===========================ĐĂNG Xuat Start=====================================
# ===========================ĐĂNG Xuat Start=====================================
@app.route('/dang-xuat', methods=['GET', 'POST'])
def dang_xuat():
    session.pop('session_username', None)
    session.pop('session_fullname', None)
    session.pop('session_id_nha_hang', None)
    session.pop('session_phan_cap', None)
    session.pop('session_brand_id', None)
    session.pop('session_district_id', None)
    session.pop('session_region_id', None)
    session.pop('session_chuoi_dang_xuat', None)
    session.pop('session_chuoi_html_nha_hang_thong_tin', None)
    session.pop('session_chuoi_html_ban_tin_hoan_thanh', None)

    return redirect(url_for('index'))
    # return render_template('login.html',USER = user1 , PASS = pass1)
# ===========================ĐĂNG Xuat END=====================================
# ===========ĐĂNG Xuat END===================



