from flask import render_template , request , Markup , url_for , redirect , session, sessions,send_file,jsonify
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
    chuoidangnhap = ''
    chuoi_html_index_brand = CHUOI_HTML_INDEX_BRAND()

    if request.form.get('user_dang_nhap'):
        username = request.form.get('user_dang_nhap')
        password = request.form.get('pass')
        check_dang_nhap = CHECK_DANG_NHAP(username, password)
        if check_dang_nhap[0] != '-1':
            session['username'] = check_dang_nhap[0]
            session['fullname'] = check_dang_nhap[1]
            session['id_nha_hang'] = check_dang_nhap[2]
            return redirect(url_for('nha_hang'))
        else:
            chuoidangnhap = '''                                        
                            <div class="alert alert-danger thong_bao" role="alert">
                                Sai Tên Đăng Nhập Hoặc Mật Khẩu
                            </div>
                            '''
            return render_template('index.html', CHUOI_HTML_HIEN_THI_INDEX_BRAND = chuoi_html_index_brand,DANG_NHAP_THAT_BAI = Markup(chuoidangnhap))

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
    if ma_brand == 'HT' or ma_brand == 'MW' or ma_brand == 'GG' or ma_brand == 'KK' or ma_brand == 'ASM'\
    or ma_brand == 'KP' or ma_brand == 'ISS' or ma_brand == 'CBJ' or ma_brand == 'DRM' or ma_brand == 'SM'\
    or ma_brand == 'YT' or ma_brand == 'ICOOK':
        chuoi_html_chi_tiet_ban_tin = CHUOI_HTML_CHI_TIET_BAN_TIN(ma_brand)
        img = IMG(ma_brand)
    else:
        chuoi_html_chi_tiet_ban_tin1 = '<h1>Trang Này Không Tồn Tại, Đừng Tự Gõ Vào Nữa Năn Nỉ Đóa.....</h1>'
        chuoi_html_chi_tiet_ban_tin = Markup(chuoi_html_chi_tiet_ban_tin1)
        img=''


    if request.form.get('user_dang_nhap'):
        print(request.form.get('user_dang_nhap'))
    return render_template('chi_tiet_ban_tin.html',CHUOI_HTML_HIEN_THI_CHI_TIET_BAN_TIN = chuoi_html_chi_tiet_ban_tin,IMG=img)








@app.route("/nha_hang", methods = ["POST","GET"])
def nha_hang():
    if session.get('username') is not None:
        username = session['username']
        fullname = session['fullname']
        id_nha_hang = session['id_nha_hang']      
        chuoi_html_ban_tin_con_su_dung  = CHUOI_HTML_NHA_HANG_BAN_TIN_CON_SU_DUNG(3)
        return render_template('Nha_Hang/nha_hang.html' , HIEN_THI_NHA_HANG_TIN_CON_SU_DUNG = chuoi_html_ban_tin_con_su_dung)
    return redirect(url_for('index'))







