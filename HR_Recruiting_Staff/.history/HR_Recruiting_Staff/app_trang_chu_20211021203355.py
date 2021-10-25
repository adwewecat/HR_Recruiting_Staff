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
    # qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=2)
    # qr.add_data(' Họ Tên : nguyen anh dung \n'+'Tuổi : 26')
    # qr.make(fit=True)
    # img = qr.make_image(fill_color='black',back_color='white')
    # img.save("/HR_Recruiting_Staff/static/images/conmeo.png")
    chuoidangnhap = ''
    chuoi_html_index_brand = CHUOI_HTML_INDEX_BRAND()

    if session.get('session_phan_cap') is not None:
        if session['session_phan_cap'] == 'nhahang':
            return redirect(url_for('nha_hang'))
        else:
            return redirect(url_for('dang_xuat'))

    if request.form.get('user_dang_nhap'):
        username = request.form.get('user_dang_nhap')
        password = request.form.get('pass')
        check_dang_nhap = CHECK_DANG_NHAP(username, password)
        if check_dang_nhap[0] != '-1':
            session['session_username'] = check_dang_nhap[0]
            session['session_fullname'] = check_dang_nhap[1]
            session['session_id_nha_hang'] = check_dang_nhap[2]
            session['session_phan_cap'] = check_dang_nhap[3]
            if check_dang_nhap[3] == 'nhahang':
                return redirect(url_for('nha_hang'))
            else:
                return redirect(url_for('dang_xuat'))
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



@app.route("/<string:ma_brand>", methods = ["POST","GET"])
def brand(ma_brand):
    chuoidangnhap=''
    if ma_brand == 'HT' or ma_brand == 'MW' or ma_brand == 'GG' or ma_brand == 'KK' or ma_brand == 'ASM'\
    or ma_brand == 'KP' or ma_brand == 'ISS' or ma_brand == 'CBJ' or ma_brand == 'DRM' or ma_brand == 'SM'\
    or ma_brand == 'YT' or ma_brand == 'ICOOK':
        chuoi_html_chi_tiet_ban_tin = CHUOI_HTML_CHI_TIET_BAN_TIN(ma_brand)
        img = IMG(ma_brand)
    else:
        chuoi_html_chi_tiet_ban_tin1 = '<h1>Trang Này Không Tồn Tại, Đừng Tự Gõ Vào Nữa Năn Nỉ Đóa.....</h1>'
        chuoi_html_chi_tiet_ban_tin = Markup(chuoi_html_chi_tiet_ban_tin1)
        img=''

    if session.get('session_phan_cap') is not None:
        if session['session_phan_cap'] == 'nhahang':
            return redirect(url_for('nha_hang'))
        else:
            return redirect(url_for('dang_xuat'))


    if request.form.get('user_dang_nhap'):
        username = request.form.get('user_dang_nhap')
        password = request.form.get('pass')
        check_dang_nhap = CHECK_DANG_NHAP(username, password)
        if check_dang_nhap[0] != '-1':
            session['session_username'] = check_dang_nhap[0]
            session['session_fullname'] = check_dang_nhap[1]
            session['session_id_nha_hang'] = check_dang_nhap[2]
            session['session_phan_cap'] = check_dang_nhap[3]
            if check_dang_nhap[3] == 'nhahang':
                return redirect(url_for('nha_hang'))
            else:
                return redirect(url_for('dang_xuat'))
        else:
            chuoidangnhap = '''                                        
                            <div class="alert alert-danger thong_bao" role="alert">
                                Sai Tên Đăng Nhập Hoặc Mật Khẩu
                            </div>
                            '''


    return render_template('chi_tiet_ban_tin.html',CHUOI_HTML_HIEN_THI_CHI_TIET_BAN_TIN = chuoi_html_chi_tiet_ban_tin,IMG=img , DANG_NHAP_THAT_BAI = Markup(chuoidangnhap))








@app.route("/nha_hang", methods = ["POST","GET"])
def nha_hang():


    if request.form.get('nhahang_dangtin_soluong'):
        nhahang_dangtin_soluong = request.form.get('nhahang_dangtin_soluong')
        nhahang_dangtin_gio_from =request.form.get('nhahang_dangtin_gio_from') 
        nhahang_dangtin_gio_to = request.form.get('nhahang_dangtin_gio_to')
        nhahang_dangtin_note_vitri = request.form.get('nhahang_dangtin_note_vitri')
        them_ban_tin = INSERT_BAN_TIN_NHA_HANG(restaurant_id,brand_id,district_id,nhahang_dangtin_note_vitri)




    if session.get('session_id_nha_hang') is not None:
        phancap = session['session_phan_cap']
        if phancap == 'nhahang':
            username = session['session_username']
            fullname = session['session_fullname']
            id_nha_hang = session['session_id_nha_hang']
            thong_tin_nha_hang = GET_THONG_TIN_NHAHANG(id_nha_hang)
            session['session_brand_id'] = thong_tin_nha_hang[0]
            session['session_district_id'] = thong_tin_nha_hang[1]
            session['session_region_id'] = thong_tin_nha_hang[2]
            chuoi_dang_xuat = GET_THONG_TIN_DANG_XUAT(phancap,id_nha_hang,fullname,username)
            chuoi_html_nha_hang_thong_tin = CHUOI_HTML_NHA_HANG_THONG_TIN(id_nha_hang)    
            chuoi_html_ban_tin_con_su_dung  = CHUOI_HTML_NHA_HANG_BAN_TIN_CON_SU_DUNG(id_nha_hang)
            chuoi_html_ban_tin_hoan_thanh  = CHUOI_HTML_NHA_HANG_BAN_TIN_HOAN_THANH(id_nha_hang)
            
            session['session_chuoi_dang_xuat'] = chuoi_dang_xuat
            session['session_chuoi_html_nha_hang_thong_tin'] = chuoi_html_nha_hang_thong_tin
            session['session_chuoi_html_ban_tin_hoan_thanh'] = chuoi_html_ban_tin_hoan_thanh
          

            return render_template('Nha_Hang/nha_hang.html' , HIEN_THI_NHA_HANG_TIN_CON_SU_DUNG = chuoi_html_ban_tin_con_su_dung , HIEN_THI_HTML_THONG_TIN_NHA_HANG = chuoi_html_nha_hang_thong_tin,HIEN_THI_HTML_THONG_TIN_NHA_HANG_HOAN_THANH = chuoi_html_ban_tin_hoan_thanh,THONG_TIN_DANG_XUAT = chuoi_dang_xuat)
    

    return redirect(url_for('dang_xuat'))







