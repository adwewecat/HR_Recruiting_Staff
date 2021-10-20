from flask import Markup, url_for
import json
import os
import sqlite3
from HR_Recruiting_Staff.thu_vien.connection import *
from datetime import datetime




# =============================== Trang Index Trang Index Brand Start ===============================
def CHUOI_HTML_INDEX_BRAND():
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = 'select\
            B.img,\
            B.ten_viet_tat,\
            A.brand_id,\
            CASE WHEN SUM(A.staff_quantity) IS NULL THEN 0\
            WHEN SUM(A.staff_quantity) IS NOT NULL THEN SUM(A.staff_quantity)\
            END "staff_quantity"\
            from [dbo].[Newpost] AS A\
            Right JOIN [dbo].[Brand] B ON B.id = A.brand_id\
            where B.active=1\
            GROUP BY A.brand_id,B.img,B.ten_viet_tat\
            Order By staff_quantity DESC\
            '
      conn_2014.execute(sql)  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              IMG = item[0]
              TEN_VIET_TAT = item[1]
              STAFF_QUANTITY = item[3]
              if STAFF_QUANTITY >=20:
                HOT = ''
              else:
                HOT = 'hide-hot'
              list_danh_sach +='''
                          <div class="col l-3 m-6 c-12">
                            <!-- hide-hot -->
                            <div class="block__product-hot '''+HOT+'''">
                              <div class="home-product-item__sale-off">
                                <span class="home-product-item__sale-off-percen">HOT</span>
                              </div>
                            </div>
                          <a href="/'''+str(TEN_VIET_TAT)+'''" class="block__product">
                            <div class="block__product-img">
                              <img
                                src="/static/images/logos/'''+str(IMG)+'''"
                                alt=""
                                class="block__product-img-item"
                              />

                            </div>
                            <div class="block__product-content">
                              <div class="block__product-content-item">
                                <span>Số Người Cần Tuyển : '''+str(STAFF_QUANTITY)+''' </span>
                              </div>
                            </div>
                          </a>
                          </div>
                              '''   
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Index Brand END ===============================
# =================




# =============================== Trang Chi Tiết Bản Tin Start ===============================
# =================
def CHUOI_HTML_CHI_TIET_BAN_TIN(brand_ten_viet_tat):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = "select\
              A.id,\
              B.img,\
              E.name,\
              FORMAT(A.time_from, 'hh') AS h_timefrom,\
              FORMAT(A.time_from, 'mm') AS m_timefrom,\
              FORMAT(A.time_to, 'hh') AS h_timeto,\
              FORMAT(A.time_to, 'mm') AS m_timeto,\
              C.district_name,\
              A.staff_quantity,\
              A.note,\
              E.sdt,\
              E.address\
              from [dbo].[Newpost] as A\
              Left Join [dbo].[Brand] AS B ON A.brand_id = B.id\
              Left Join [dbo].[District] AS C ON A.district_id = C.id\
              Left Join [dbo].[Regions] AS D ON A.region_id = D.id\
              Left Join [dbo].[Restaurants] AS E ON A.restaurant_id = E.id\
              where\
              B.ten_viet_tat = ?\
              AND A.active=1"
      conn_2014.execute(sql,brand_ten_viet_tat)  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              ID = item[0]
              IMG = item[1]
              NAME = item[2]
              H_TIME_FROM = item[3]
              M_TIME_FROM = item[4]
              H_TIME_TO = item[5]
              M_TIME_TO = item[6]
              DISTRICT_NAME = item[7]
              STAFF_QUANTITY = item[8]
              NOTE = item[9]
              if NOTE == None:
                NOTE ='..........'
              SDT = item[10]
              ADDRESS = item[11]
              list_danh_sach +='''
                            <div class="col l-6 m-6 c-12">
                              <a class="new__post-item-link" data-toggle="modal" data-target="#ban_tin'''+str(ID)+'''">
                                  <div class="new__post-item-img">
                                  <img src="/static/images/logos/'''+str(IMG)+'''" alt="" class="new__post-item-img-link">
                                  </div>
                                  <div class="new__post-content-list">
                                    <div class="new__post-content-item-res">
                                      <span class=" new__post-content-item new__post-content-item-name">'''+str(NAME)+'''</span>
                                    </div>
                                    <div class="new__post-content-list-comment">
                                      <div class="new__post-content-list-time">
                                        <div class="new__postlist-time">
                                          <span class="new__post-content-list-comment-item">Thời Gian Làm :</span>
                                          <span class="new__post-content-list-comment-item">'''+str(H_TIME_FROM)+''':'''+str(M_TIME_FROM)+'''</span>
                                          
                                            <i class="fas fa-arrow-right new__post-content-list-comment-item"></i>

                                          <span class="new__post-content-list-comment-item">'''+str(H_TIME_TO)+''':'''+str(M_TIME_TO)+'''</span>
                                        </div>
                                        <div class="new__postlist-vitri">
                                          <span class="new__post-content-list-comment-item">Vị Trí : '''+str(NOTE)+'''</span>
                                        </div> 
                                      </div>
                                      <div class="new__post-content-list-comment-item-quantity">
                                        <span class="new__post-content-list-comment-item new__post-content-list-comment-item--diadiem">Địa Điểm :'''+str(DISTRICT_NAME)+'''</span>
                                        <span class="new__post-content-list-comment-item quantity-cach-le">Cần Tuyển : <span style="color:red">'''+str(STAFF_QUANTITY)+'''</span> Bạn</span>
                                      </div>
                                    </div>

                                  </div>
                              </a>
                            </div>
                                <!-- Modal Start-->
                                <div class="modal fade" id="ban_tin'''+str(ID)+'''" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                  <div class="modal-dialog modal-dialog-centered" role="document">
                                    <div class="modal-content">
                                      <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLongTitle">'''+str(NAME)+'''</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                          <span aria-hidden="true">&times;</span>
                                        </button>
                                      </div>
                                      <div class="modal-body">
                                        <div class="modal-note">
                                          <span>Vị Trí : '''+str(NOTE)+'''</span>
                                        </div>
                                        <div class="modal-address">
                                          <span>Liên Hệ : <a href="tel:'''+str(SDT)+'''">'''+str(SDT)+''' 
                                          <i class="fas fa-phone-square icon__phone"></i> </a></span>
                                        </div>
                                        <div class="">
                                          <span>Địa Chỉ :'''+str(ADDRESS)+'''</span>
                                        </div>
                                      </div>
                                      <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                        <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
                                      </div>
                                    </div>
                                  </div>
                                </div>
                                <!-- Modal End-->
                              '''   
      connection_2014.close()                          
    else:
        list_danh_sach =' <h1 type="color:red"> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Chi Tiết Bản Tin END ===============================
# =================



# =============================== Trang Index Trang Index Brand Start ===============================
def IMG(ten_viet_tat_brand):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = 'SELECT top 1 img FROM [dbo].[Brand] where active=1 AND ten_viet_tat = ? order by stt'
      conn_2014.execute(sql,ten_viet_tat_brand)  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              IMG = item[0]
              list_danh_sach = 'src="/static/images/logos/' + str(IMG) + '"'
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Index Brand END ===============================
# =================





# =============================== Trang Index Trang Index Brand Start ===============================
def CHUOI_HTML_NHA_HANG_BAN_TIN_CON_SU_DUNG(restaurant_id):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = "SELECT\
              id,\
              note,\
              staff_quantity,\
              FORMAT(time_from, 'hh') AS h_timefrom,\
              FORMAT(time_from, 'mm') AS m_timefrom,\
              FORMAT(time_to, 'hh') AS h_timeto,\
              FORMAT(time_to, 'mm') AS m_timeto\
              FROM [dbo].[Newpost]\
              WHERE\
              restaurant_id = ?\
              AND active = 1\
            "
      conn_2014.execute(sql,(restaurant_id,))  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              ID = item[0]
              NOTE = item[1]
              STAFF_QUANTITY = item[2]
              H_TIME_FROM = item[3]
              M_TIME_FROM = item[4]
              H_TIME_TO = item[5]
              M_TIME_TO = item[6]
              list_danh_sach +='''
                                  <div class="l-6 c-12">
                                    <a class="nha_hang_danh_sach__new-item" data-toggle="modal"
                                      data-target="#ban_tin'''+str(ID)+'''">
                                      <div class="nhahang__new--time">
                                        <span class="nhahang__new--time-item">
                                          Thời Gian : '''+str(H_TIME_FROM)+''':'''+str(M_TIME_FROM)+'''
                                          <i class="fas fa-arrow-right"></i>
                                          '''+str(H_TIME_TO)+''':'''+str(M_TIME_TO)+'''
                                        </span>
                                      </div>
                                      <div class="nhahang__new--vitri">
                                        <span class="nhahang__new--vitri-item">
                                          Vị Trí : '''+str(NOTE)+'''
                                        </span>
                                        <span class="nhahang__new--vitri-item nhahang__new--vitri-item-soluong">
                                          Số Lượng : '''+str(STAFF_QUANTITY)+'''
                                        </span>
                                      </div>
                                    </a>
                                  </div>
                                  <!-- Modal Start-->
                                  <div class="modal fade" id="ban_tin'''+str(ID)+'''" tabindex="-1" role="dialog"
                                    aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered" role="document">
                                      <div class="modal-content">
                                        <div class="modal-header">
                                          <h5 class="modal-title" id="exampleModalLongTitle">Hoàn Thành Bài Đăng Tuyền Dụng</h5>
                                          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                          </button>
                                        </div>
                                        <form method="post">
                                        <div class="modal-body">
                                          <div class="modal-note">
                                            <div class="nha_hang_bantin_new__soluong-thuc">
                                              <input class="nha_hang_bantin_new__soluong-thuc-item" type="number" min="1" name="so_luong_thuc_te"
                                                placeholder="Số Lượng Người Thực Tế Tuyển Được" value="'''+str(STAFF_QUANTITY)+'''" required>
                                            </div>
                                            <input name='ID' type="text" value="'''+str(ID)+'''" hidden>
                                          </div>
                                        </div>
                                        <div class="modal-footer">
                                          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                          <button type="submit" class="button__dang-tin-item">Hoàn Thành</button>
                                        </div>
                                      </form>
                                      </div>
                                    </div>
                                  </div>
                                  <!-- Modal End-->
                              '''   
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Index Brand END ===============================
# =================





# =============================== Trang Nhà Hàng Thông Tin Start ===============================
def CHUOI_HTML_NHA_HANG_THONG_TIN():
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = 'select top 1 name,address,sdt from [dbo].[Restaurants] where id= ? '
      conn_2014.execute(sql)  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              IMG = item[0]
              TEN_VIET_TAT = item[1]
              STAFF_QUANTITY = item[3]
              if STAFF_QUANTITY >=20:
                HOT = ''
              else:
                HOT = 'hide-hot'
              list_danh_sach +='''
                          <div class="col l-3 m-6 c-12">
                            <!-- hide-hot -->
                            <div class="block__product-hot '''+HOT+'''">
                              <div class="home-product-item__sale-off">
                                <span class="home-product-item__sale-off-percen">HOT</span>
                              </div>
                            </div>
                          <a href="/'''+str(TEN_VIET_TAT)+'''" class="block__product">
                            <div class="block__product-img">
                              <img
                                src="/static/images/logos/'''+str(IMG)+'''"
                                alt=""
                                class="block__product-img-item"
                              />

                            </div>
                            <div class="block__product-content">
                              <div class="block__product-content-item">
                                <span>Số Người Cần Tuyển : '''+str(STAFF_QUANTITY)+''' </span>
                              </div>
                            </div>
                          </a>
                          </div>
                              '''   
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Nhà Hàng Thông Tin END ===============================
# =================





def CHECK_DANG_NHAP(ten_dang_nhap, mat_khau):
    list_dang_nhap = [ '-1','-1','-1','-1']
    connection_2014 = connect_database_SQL_2014()

    conn_2014 = connection_2014.cursor()
    sql = "select top 1 username, fullname,nha_hang,phan_cap from [dbo].[User_all]\
            where username =?\
            and pass =?\
            and active=1\
          "
    conn_2014.execute(sql,(ten_dang_nhap,mat_khau,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
          list_dang_nhap.clear()
          list_dang_nhap.append(item[0])
          list_dang_nhap.append(item[1])
          list_dang_nhap.append(item[2])
          list_dang_nhap.append(item[3])
    return list_dang_nhap


























def XU_LY_DANG_NHAP(ten_dang_nhap, mat_khau):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT PHAN_LOAI,MA_NHAN_VIEN,PHONG_BAN FROM DB_USER WHERE _USER_NAME =? AND PASS =? AND ACTIVE = '1' LIMIT 1;"
    ket_qua = conn.execute(chuoi_sql, (ten_dang_nhap, mat_khau))
    list_dang_nhap = [ '-1','-1','-1']
    hop_le = ''
    # print(ket_qua)
    if ket_qua is not None:
        for ten in ket_qua:
            list_dang_nhap.clear()
            list_dang_nhap.append(ten[0])
            list_dang_nhap.append(ten[1])
            list_dang_nhap.append(ten[2])
        # print(list_dang_nhap)
    conn.close()
    return list_dang_nhap




def CHUOI_HTML_DANG_XUAT(ten):
    chuoi_html_dang_nhap = ''
    chuoi_html_dang_nhap += '<div class="dropdown">'
    chuoi_html_dang_nhap += '<button style="background-color:#ffda3d; border:none; " class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+ten
    chuoi_html_dang_nhap += '  </button>'
    chuoi_html_dang_nhap += '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
    chuoi_html_dang_nhap += '<a class="dropdown-item" href="/dang-xuat">Đăng Xuất</a>'
    chuoi_html_dang_nhap += '</div>'
    chuoi_html_dang_nhap += '</div>'

    return Markup(chuoi_html_dang_nhap)




# =============================== Trang Index Báo Cáo Lưu File USER Start ===============================
def CHUOI_HTML_DANH_SACH_FILE_MOI_LUU(user_dang_nhap):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = 'SELECT TOP 10 id,ten_file_luu,data,ngay_het_han,ten_chung_tu,ten_file_luu FROM UPLOAD_FILE_MANAGERMENT WHERE user_them = ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(user_dang_nhap,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            ID = item[0]
            TEN = item[1]
            DATA = item[2]
            NGAY_HET_HAN = item[3]
            TEN_CHUNG_TU = item[4]
            TEN_FILE_LUU = item[5]
            list_danh_sach +='''
                                <tr>
                                <form method="POST" enctype="multipart/form-data">
                                <div class="form-group">
                                    <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(ID)+'''">
                                    <h5 align="center">'''+str(TEN_CHUNG_TU)+'''</h5>
                                    <div class="row" >
                                    <div class="col-md-8">
                                    <h8 align="left">Ngày Hết Hạn Hợp Đồng : '''+str(NGAY_HET_HAN)+''' </h8>
                                    </div>
                                    <div class="col-md-3">
                                    <button type="submit" style="background-color:#DAA520; color:black" >Dowload File</a>
                                    </div>

                                </div>
                                <div class="row" >
                                <div class="col-md-8">
                                '''+str(TEN_FILE_LUU)+'''
                                </div>
                                </div>
                                ----------------------------------------------------------------
                                </div>
                                            </form>
                                            </tr>
                            '''
    return Markup(list_danh_sach)
# =============================== Trang Index Báo Cáo Lưu File USER END ===============================
# =================



# =============================== Trang Index Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_DANH_SACH_FILE_MOI_LUU_TRUONG_PHONG(phong_ban):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = 'SELECT TOP 10 id,ten_file_luu,data,ngay_het_han,ten_chung_tu,ten_file_luu FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(phong_ban,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            ID = item[0]
            TEN = item[1]
            DATA = item[2]
            NGAY_HET_HAN = item[3]
            TEN_CHUNG_TU = item[4]
            TEN_FILE_LUU = item[5]
            list_danh_sach +='''
                                <tr>
                                <form method="POST" enctype="multipart/form-data">
                                <div class="form-group">
                                    <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(ID)+'''">
                                    <h5 align="center">'''+str(TEN_CHUNG_TU)+'''</h5>
                                    <div class="row" >
                                    <div class="col-md-8">
                                    <h8 align="left">Ngày Hết Hạn Hợp Đồng : '''+str(NGAY_HET_HAN)+''' </h8>
                                    </div>
                                    <div class="col-md-3">
                                    <button type="submit" style="background-color:#DAA520; color:black" >Dowload File</a>
                                    </div>

                                </div>
                                <div class="row" >
                                <div class="col-md-8">
                                '''+str(TEN_FILE_LUU)+'''
                                </div>
                                </div>
                                ----------------------------------------------------------------
                                </div>
                                            </form>
                                            </tr>
                            '''
    return Markup(list_danh_sach)
# =============================== Trang Index Báo Cáo Lưu File TRƯỞNG PHÒNG END ===============================
# =================





# =============================== Check-FILE LƯU CÓ TỒN TẠI HAY CHƯA USER START ===============================
# =================
def CHECK_FILE_LUU_CO_TON_TAI_HAY_CHUA(user_dang_nhap,ten_chung_tu):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = 'SELECT id,ten_chung_tu FROM UPLOAD_FILE_MANAGERMENT WHERE user_them = ? AND ten_chung_tu = ?'
    conn_2014.execute(sql,(user_dang_nhap,ten_chung_tu,))  
    danh_sach = conn_2014.fetchall()   
    list_danh_sach = ['-1', '-1']
    if danh_sach is not None:
        for item in danh_sach:
            list_danh_sach.clear()
            list_danh_sach.append(str(item[0]))
            list_danh_sach.append(item[1])
        # print(list_danh_sach)
    conn_2014.close()
    return list_danh_sach
# =============================== Check-FILE LƯU CÓ TỒN TẠI HAY CHƯA USER END ===============================
# =================




# =============================== Check-FILE LƯU CÓ TỒN TẠI HAY CHƯA TRƯỞNG PHÒNG START ===============================
# =================
def CHECK_FILE_LUU_CO_TON_TAI_HAY_CHUA_TRUONG_PHONG(phong_ban,ten_chung_tu):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = 'SELECT id,ten_chung_tu FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? AND ten_chung_tu = ?'
    conn_2014.execute(sql,(phong_ban,ten_chung_tu,))  
    danh_sach = conn_2014.fetchall()   
    list_danh_sach = ['-1', '-1']
    if danh_sach is not None:
        for item in danh_sach:
            list_danh_sach.clear()
            list_danh_sach.append(str(item[0]))
            list_danh_sach.append(item[1])
        # print(list_danh_sach)
    conn_2014.close()
    return list_danh_sach
# =============================== Check-FILE LƯU CÓ TỒN TẠI HAY CHƯA TRƯỞNG PHÒNG END ===============================
# =================





# =============================== Danh sách user - quản trị admin Start ===============================
def CHUOI_HTML_DANH_SACH_USER_ADMIN():
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT * FROM DB_USER WHERE _USER_NAME NOT IN ('ADMIN') "
    chuoi_html_danh_sach_user_admin = ''
    ket_qua = conn.execute(chuoi_sql)
    if ket_qua is not None:
        for list1 in ket_qua:
            checkmacdinh1 = ''
            checkmacdinh2 = ''
            checkmacdinh3 = ''
            checkmacdinh4 = ''
            checkmacdinh5 = ''
            checkmacdinh6 = ''
            checkmacdinh7 = ''
            checkmacdinh8 = ''
            checkmacdinh9 = ''
            checkmacdinh10 = ''
            checkmacdinh11 = ''
            checkmacdinh12 = ''
            checkmacdinh13 = ''
            checkmacdinh14 = ''
            _id = list1[0]
            user = list1[1]
            pass1 = list1[2]
            phanloai = list1[3]
            ma_nhan_vien = list1[5]
            if phanloai == 'QUANTRI':
                checkmacdinh1 = 'selected="selected"'
                phanloai='Quản Trị'
            elif phanloai =='NHAHANG':
                checkmacdinh2 = 'selected="selected"'
                phanloai='Nhà Hàng' 
            elif phanloai =='USERCANHAN':
                checkmacdinh3 = 'selected="selected"'
                phanloai='User Cá Nhân'   
            elif phanloai =='QUANLYFILE':
                checkmacdinh4 = 'selected="selected"'
                phanloai='QUẢN LÝ FILE' 
            elif phanloai =='HR':
                checkmacdinh5 = 'selected="selected"'
            elif phanloai =='TRUONG_PHONG':
                checkmacdinh12 = 'selected="selected"'                              

            active = list1[4]
            if active == '1':
                active='Còn Hoạt Động'
                checkmacdinh6 = 'selected="selected"'
            else:
                active ="Ngưng Hoạt Động"
                checkmacdinh7 = 'selected="selected"'
            phong_ban = list1[6]
            if phong_ban == '0':
                checkmacdinh8 = 'selected="selected"'
            elif phong_ban =='HR':
                checkmacdinh9 = 'selected="selected"'
            elif phong_ban =='Legal':
                checkmacdinh10 = 'selected="selected"'           
            elif phong_ban =='SC':
                checkmacdinh11 = 'selected="selected"'
            chuoi_html_danh_sach_user_admin +='''
 
             <tbody id="myTable">
                <tr>
                  <td width="100">'''+user+'''</td>
                  <td width="120" style="color :red;"><b>'''+phanloai+'''</b></td>
                  <td width="250">'''+active+'''</td>
                  <td width="80"><a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#DELETE'''+str(_id)+'''" data-toggle="modal"> DELETE </a> </td>
                  <td width="80"><a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#INSERT" data-toggle="modal"> INSERT </a></td>
                  <td width="80"><a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a></td>
                </tr>
              </tbody>


          <!--Modal: modalConfirm DELETE-->
            <div class="modal fade" id="DELETE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
              aria-labelledby="staticBackdropLabel" aria-hidden="true">
              <div class="modal-dialog" role="document">
                <div class="modal-content">

              <div class="modal-header" style="text-align:center;">
                <h5 class="modal-title" id="exampleModalLabel">Delete User</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <form method="POST" enctype="multipart/form-data">
                  <div class="form-group">
                    <label for="recipient-name" class="col-form-label">User Name:(*)</label>
                    <input name="user_delete" type="text" class="form-control" id="recipient-name" value="'''+user+'''" required disabled>
                    <input type="hidden" name="txt_id_delete" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    <input type="hidden" name="user_delete" style="height:0px;width:0px;" value="'''+user+'''">
                  </div>

                  <div class="form-group">
                    <label for="recipient-name" class="col-form-label">Ghi Chú:</label>
                    <textarea name="ghi_chu" type="text" class="form-control" id="recipient-name" ></textarea>
                    <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                  </div>            


                  <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Delete</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                    </div>

                  </form>

              </div>
            </div>
          </div>
          </div>
          <!--Modal: modalConfirm DELETE-->



                <!--Modal: modalConfirm INSERT-->
                <div class="modal fade" id="INSERT" data-backdrop="static" tabindex="-1" role="dialog"
                  aria-labelledby="staticBackdropLabel" aria-hidden="true">
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">

                      <div class="modal-header" style="text-align:center;">
                        <h5 class="modal-title" id="exampleModalLabel">Insert User</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      <div class="modal-body">
                        <form method="POST" enctype="multipart/form-data">

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">User Name:(*)</label>
                            <input name="user_insert" type="text" class="form-control" id="recipient-name" required>
                            <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                          </div>

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">PASSWORD:(*)</label>
                            <input name="pass_insert" type="password" class="form-control" id="recipient-name" required>
                          </div>

                           <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                            <input name="ma_nhan_vien_insert" type="text" class="form-control" id="recipient-name" required>
                          </div>                         

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">PHÂN QUYỀN:(*)</label>
                            <select name="phanquyen_insert" class="form-control">
                              <option label="QUẢN TRỊ">QUANTRI</option>
                              <option label="Quản Lý File">QUANLYFILE</option>
                              <option label="USER CÁ NHÂN ">USERCANHAN</option>
                              <option label="NHÂN SỰ (HR)">HR</option>
                              <option selected="selected" label="NHÀ HÀNG">NHAHANG</option>
                              <option label="TRƯỞNG PHÒNG">TRUONG_PHONG</option>
                            </select>

                          </div>
                     

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">ACCTIVE:(*)</label>
                            <div class="form-group">
                              <select name="active_insert" class="form-control">
                                <option label="Kích Hoạt">1</option>
                                <option selected="selected" label="Không Kích Hoạt">0</option>

                              </select>
                            </div>

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Phòng Ban:(*)</label>
                            <div class="form-group">
                              <select name="phong_ban_insert" class="form-control">
                              <option label="Khác">0</option>
                                <option label="MKT">MKT</option>
                                <option label="Legal">Legal</option>
                                <option label="SC">SC</option>
                              </select>
                            </div>

                            </div>

                            <div class="modal-footer">
                              <button type="submit" class="btn btn-primary">Insert</button>
                              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                            </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>
                <!--Modal: modalConfirm INSERT-->
          </div>
          </form>


          <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update User</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">User Name:(*)</label>
                      <input name="user_update1" type="text" class="form-control" id="recipient-name" value="'''+user+'''" required disabled>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                      <input type="hidden" name="user_update" style="height:0px;width:0px;" value="'''+user+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">PASS WORD:(*)</label>
                      <input name="password_update" type="password" class="form-control" id="recipient-name" value ="'''+pass1+'''" required>
                    </div>

                    <div class="form-group">
                    <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                    <input name="ma_nhan_vien_update" type="text" class="form-control" id="recipient-name" value = "'''+str(ma_nhan_vien)+'''" required>
                  </div>                        

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">PHÂN QUYỀN:(*)</label>
                      <select name="phanquyen_update" class="form-control">
                        <option label="QUẢN TRỊ" '''+str(checkmacdinh1)+'''>QUANTRI</option>
                        <option label="Quản Lý File" '''+str(checkmacdinh4)+'''>QUANLYFILE</option>
                        <option label="USER CÁ NHÂN" '''+str(checkmacdinh3)+'''>USERCANHAN</option>
                        <option label="NHÂN SỰ (HR)" '''+str(checkmacdinh5)+'''>HR</option>
                        <option label="NHÀ HÀNG" '''+str(checkmacdinh2)+'''>NHAHANG</option>
                        <option label="TRƯỞNG PHÒNG" '''+str(checkmacdinh12)+'''>TRUONG_PHONG</option>                       
                      </select>

                    </div>


                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">ACCTIVE:(*)</label>
                      <div class="form-group">
                        <select name="trangthai_update" class="form-control">
                          <option label="Kích Hoạt" '''+str(checkmacdinh6)+'''>1</option>
                          <option label="Không Kích Hoạt" '''+str(checkmacdinh7)+'''>0</option>

                        </select>

                      </div>
                      
                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Phòng Ban:(*)</label>
                            <div class="form-group">
                              <select name="phong_ban_update" class="form-control">
                              <option label="Khác" '''+str(checkmacdinh8)+'''>0</option>
                                <option label="HR" '''+str(checkmacdinh9)+'''>HR</option>
                                <option label="Legal" '''+str(checkmacdinh10)+'''>Legal</option>
                                <option label="SC" '''+str(checkmacdinh11)+'''>SC</option>
                              </select>
                            </div>
                            </div>

                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                  </form>
                </div>

              </div>
            </div>
          </div>
          <!--Modal: modalConfirm UPDATE-->
          </form>
            </div>

            '''
    conn.close()
    return Markup(chuoi_html_danh_sach_user_admin)
# =============================== Danh sách user - quản trị admin End ===============================
# ===================




# =============================== Check-Insert Nhân Viên Start ===============================
def CHECK_INSERT_NHAN_VIEN(ten_dang_nhap):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT _USER_NAME FROM DB_USER WHERE _USER_NAME =?"
    ket_qua = conn.execute(chuoi_sql, (ten_dang_nhap,))
    list_dang_nhap = '-1'
    # print(ket_qua)
    if ket_qua is not None:
        for ten in ket_qua:
            list_dang_nhap = ten[0]
        # print(list_dang_nhap)
    conn.close()
    return list_dang_nhap
# =============================== Check-Insert Nhân Viên END ===============================
# =================



# ===============================Danh sách LOGS Start ===============================
def CHUOI_HTML_DANH_SACH_LOGS():
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT * FROM DB_LOGS ORDER BY thoi_gian DESC"
    chuoi_html_danh_sach_logs = 'Không Có Dữ Liệu LOGS'
    ket_qua = conn.execute(chuoi_sql)
    if ket_qua is not None:
        chuoi_html_danh_sach_logs = ''
        for list1 in ket_qua:
            _id = list1[0]
            noi_dung = list1[1]
            chuc_nang = list1[2]
            thoi_gian = list1[3]
            user_thuc_hien = list1[4]
            chuoi_html_danh_sach_logs +='''
                <tr>
                  <th width="40">'''+str(_id)+''' </th>
                  <th width="250">'''+noi_dung+'''</th>
                  <th width="100">'''+chuc_nang+'''</th>
                  <th width="100">'''+thoi_gian+'''</th>
                  <th width="130">'''+user_thuc_hien+'''</th>
                </tr>
            '''


    conn.close()
    return Markup(chuoi_html_danh_sach_logs)
# =============================== Danh sách LOGS END ===============================
# =================




# =============================== Danh Sách Nhân Viên Tiếp Khách Start ===============================
def DANH_SACH_NHAN_VIEN_TIEP_KHACH():
    chuoi_html_danh_sach_tiep_khach = ''
    connection = connect_database()
    print ("connect successful!!")
    conn = connection.cursor()
    sql = 'SELECT A.id, A.clm_mem_id , A.clm_card_no,A.name_on_pos,A.granted_amount,A.is_unlimited,A.status,staff_code\
            FROM staff_credits AS A \
            ORDER BY A.clm_card_no DESC'

    conn.execute(sql)
    danh_sach = conn.fetchall()
    for item in danh_sach:
        # print(item['clm_mem_id'])

        _id = item['id']
        clm_mem_id = item['clm_mem_id']
        clm_card_no = item['clm_card_no']
        name_on_pos = item['name_on_pos']
        granted_amount = round(item['granted_amount'])
        active = item['status']
        moma = 'ABC'+str(_id)
        manhan_vien = item['staff_code']
        if active == 1:
            active = 'Hoạt Động'
        else:
            active = 'Ngưng Hoạt Động'

        is_unlimited = item['is_unlimited']
        # print(is_unlimited)
        if is_unlimited == 1:
            co_gioi_han_khong = 'Không Giới Hạn'
            # td = 'class="table-danger"'
        else:
            co_gioi_han_khong = 'Có Hạn Mức'  

        chuoi_html_danh_sach_tiep_khach += '''
            <tbody id="myTable">
              <th width="250">'''+name_on_pos+'''</th>
              <th width="120">'''+str(clm_card_no)+'''</th>
              <th width="100">{:,}'''.format(granted_amount).replace(",", ".")+'''</th>
              <th width="100">'''+co_gioi_han_khong+'''</th>
              <th width="100">'''+active+'''</th>
              <th width="130">
                <a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#UPDATE'''+moma+'''" data-toggle="modal"> UPDATE </a>
                      <a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#INSERT" data-toggle="modal"> INSERT </a>
              </th>
              </tr>
              <!--Modal: modalConfirm INSERT-->
              <div class="modal fade" id="INSERT" data-backdrop="static" tabindex="-1" role="dialog"
                aria-labelledby="staticBackdropLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                  <div class="modal-content">

                    <div class="modal-header" style="text-align:center;">
                      <h5 class="modal-title" id="exampleModalLabel">Insert User</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-body">
                      <form method="POST" enctype="multipart/form-data">

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">MemID:(*)</label>
                          <input name="Thclm_memid_insert" type="text" class="form-control" id="recipient-name" required>
                          <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Tên Nhân Viên:(*)</label>
                          <input name="tennhanvien_insert" type="text" class="form-control" id="recipient-name" required>
                          <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                          <input name="manhanvien_insert" type="text" class="form-control" id="recipient-name" required>
                          <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">CardNo:(*)</label>
                          <input name="card_no_insert" type="text" class="form-control" id="recipient-name" required>
                        </div>
                        
                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Hạn Mức:(*)</label>
                          <input name="hanmuc_insert" type="text" class="form-control" id="recipient-name" required>
                        </div>                        


                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Giới Hạn:(*)</label>
                          <select name="gioihan_insert" class="form-control">
                            <option label="Không Giới Hạn">1</option>
                            <option selected="selected" label="Có Giới Hạn">0</option>
                          </select>
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">ACCTIVE:(*)</label>
                          <div class="form-group">
                            <select name="kichhoat_insert" class="form-control">
                              <option label="Kích Hoạt">1</option>
                              <option selected="selected" label="Không Kích Hoạt">0</option>
                            </select>

                          </div>
                        </div>

                        <div class="modal-footer">
                          <button type="submit" class="btn btn-primary">Insert</button>
                          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                        </div>

                      </form>
                    </div>

                  </div>
                </div>
              </div>
              <!--Modal: modalConfirm INSERT-->
        </div>
        </form>


        <!--Modal: modalConfirm UPDATE-->
        <div class="modal fade" id="UPDATE'''+moma+'''" data-backdrop="static" tabindex="-1" role="dialog"
          aria-labelledby="staticBackdropLabel" aria-hidden="true">
          <div class="modal-dialog" role="document">
            <div class="modal-content">

              <div class="modal-header" style="text-align:center;">
                <h5 class="modal-title" id="exampleModalLabel">Update User</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <form method="POST" enctype="multipart/form-data">

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">MemID:(*)</label>
                          <input name="Thclm_memid_update" type="text" class="form-control" id="recipient-name" value ="'''+str(clm_mem_id)+'''" required disabled>
                          <input type="hidden" name="Thclm_memid_update" style="height:0px;width:0px;" value ="'''+str(clm_mem_id)+'''">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Tên Nhân Viên:(*)</label>
                          <input name="tennhanvien_update" type="text" class="form-control" id="recipient-name"value ="'''+name_on_pos+'''" required>
                          <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                          <input name="manhanvien_update" type="text" class="form-control" id="recipient-name"value ="'''+str(manhan_vien)+'''" required>
                          <input type="hidden" name="txt_" style="height:0px;width:0px;" value="1">
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">CardNo:(*)</label>
                          <input name="card_no_update" type="text" class="form-control" id="recipient-name"value ="'''+str(clm_card_no)+'''" required>
                        </div>
                        
                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Hạn Mức:(*)</label>
                          <input name="hanmuc_update" type="text" class="form-control" id="recipient-name" value ="'''+str(granted_amount)+'''" required>
                        </div>                        


                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">Giới Hạn:(*)</label>
                          <select name="gioihan_update" class="form-control">
                            <option label="Không Giới Hạn">1</option>
                            <option selected="selected" label="Có Giới Hạn">0</option>
                          </select>
                        </div>

                        <div class="form-group">
                          <label for="recipient-name" class="col-form-label">ACCTIVE:(*)</label>
                          <div class="form-group">
                            <select name="kichhoat_update" class="form-control">
                              <option label="Kích Hoạt">1</option>
                              <option selected="selected" label="Không Kích Hoạt">0</option>
                            </select>

                          </div>
                        </div>

                        <div class="modal-footer">
                          <button type="submit" class="btn btn-primary">Update</button>
                          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                        </div>

                </form>
              </div>

            </div>
          </div>
        </div>
        <!--Modal: modalConfirm UPDATE-->
        </form>
  </div>

  </tbody>

        '''
    conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Danh sách Nhân Viên Tiếp Khách End ===============================
# =================







# =============================== Báo Cáo Tiếp Khách Số Dư Start ===============================
def BAO_CAO_TIEP_KHACH_SO_DU():
    chuoi_html_danh_sach_tiep_khach = ''
    connection = connect_database()
    print ("connect successful!!")
    conn = connection.cursor()
    sql = 'SELECT A.name_on_pos,B.year,B.month,B.granted_amount,B.amount , (B.granted_amount - B.amount) AS "CON_LAI" \
                from staff_monthly_credits AS B , staff_credits AS A \
                where YEAR(NOW()) = B.year AND MONTH(NOW()) = B.month AND B.clm_mem_id =  A.clm_mem_id \
                ORDER BY A.clm_mem_id , B.month  DESC' \

    conn.execute(sql)
    danh_sach = conn.fetchall()
    for item in danh_sach:
        # print(item['clm_mem_id'])

        name_on_pos = item['name_on_pos']
        year = item['year']
        month = item['month']
        han_muc = round(item['granted_amount'])
        da_dung = round(item['amount'])
        CON_LAI = round(item['CON_LAI'])

        chuoi_html_danh_sach_tiep_khach += '''
                <tr>
          <th width="240">'''+name_on_pos+'''</th>
          <th width="100">'''+str(year)+'''/'''+str(month)+'''</th>
          <th width="100">{:,}'''.format(han_muc).replace(",", ".")+'''</th>
          <th width="100">{:,}'''.format(da_dung).replace(",", ".")+'''</th>
          <th width="100">{:,}'''.format(CON_LAI).replace(",", ".")+'''</th>
        </tr>
        '''

    conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Báo Cáo Tiếp Khách Số Dư  End ===============================
# =================




# =============================== Báo Cáo Chi Tiết Tiếp Khách Start ===============================
def BAO_CAO_TIEP_KHACH_CHI_TIET():
    chuoi_html_danh_sach_tiep_khach = ''
    connection = connect_database()
    print ("connect successful!!")
    conn = connection.cursor()
    sql = 'SELECT D.name_on_pos,D.clm_card_no,D.clm_mem_id,A.check_number,A.total_bill_value,E.amount AS "TIEN_TIEPKHACH",\
            A.total_pay_sum,A.pos_close_transaction_time,B.name \
            FROM pos_transactions AS A  \
            INNER JOIN restaurants AS B ON A.restaurant_code = B.code \
						INNER JOIN staff_credits AS D ON A.clm_mem_id = D.clm_mem_id \
            INNER JOIN pos_transaction_payment_details AS E ON A.id = E.transaction_id \
            where \
            MONTH(NOW()) = MONTH(A.create_time) \
						AND YEAR(NOW()) = YEAR(A.create_time) \
            AND D.clm_card_no LIKE %s \
            AND E.rk_payment_code = "390" \
            ORDER BY D.clm_mem_id,A.pos_close_transaction_time DESC' \

    conn.execute(sql,str('71080%'))
    danh_sach = conn.fetchall()
    for item in danh_sach:
        # print(item['clm_mem_id'])

        name_on_pos = item['name_on_pos']
        clm_card_no = item['clm_card_no']
        clm_mem_id = item['clm_mem_id']
        check_number = item['check_number']
        total_bill_value = round(item['total_bill_value'])
        total_pay_sum = round(item['TIEN_TIEPKHACH'])
        pos_close_transaction_time = item['pos_close_transaction_time']
        ten_nhahang = item['name']

        chuoi_html_danh_sach_tiep_khach += '''
        <tr>
          <th width="200">'''+name_on_pos+'''</th>
          <th width="150">'''+str(clm_card_no)+'''</th>
          <th width="70">'''+str(clm_mem_id)+'''</th>
          <th width="70">'''+str(check_number)+'''</th>
          <th width="100">{:,}'''.format(total_bill_value).replace(",", ".")+'''</th>
          <th width="100">{:,}'''.format(total_pay_sum).replace(",", ".")+'''</th>
          <th width="100">'''+str(pos_close_transaction_time)+'''</th>
          <th width="100">'''+ten_nhahang+'''</th>
          </tr>
        '''

    conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Báo Cáo Chi Tiết Tiếp Khách  End ===============================
# =================






# =============================== Báo Cáo Chi Tiết Theo Ngày Start ===============================
def BAO_CAO_TIEP_KHACH_CHI_TIET_THEO_NGAY(tungay , denngay):
    chuoi_html_danh_sach_tiep_khach = ''
    connection = connect_database()
    print ("connect successful!!")
    conn = connection.cursor()
    sql = 'SELECT D.name_on_pos,D.clm_card_no,D.clm_mem_id,A.check_number,A.total_bill_value,E.amount AS "TIEN_TIEPKHACH",\
            A.total_pay_sum,A.pos_close_transaction_time,B.name \
            FROM pos_transactions AS A  \
            INNER JOIN restaurants AS B ON A.restaurant_code = B.code \
						INNER JOIN staff_credits AS D ON A.clm_mem_id = D.clm_mem_id \
            INNER JOIN pos_transaction_payment_details AS E ON A.id = E.transaction_id \
            where \
						A.create_time >= %s \
  				  AND A.create_time <= %s \
            AND D.clm_card_no LIKE %s \
            AND E.rk_payment_code = "390"\
            ORDER BY D.clm_mem_id,A.pos_close_transaction_time DESC' \

    conn.execute(sql , (str(tungay),str(denngay),str('71080%')))
    danh_sach = conn.fetchall()
    for item in danh_sach:
        # print(item['clm_mem_id'])

        name_on_pos = item['name_on_pos']
        clm_card_no = item['clm_card_no']
        clm_mem_id = item['clm_mem_id']
        check_number = item['check_number']
        total_bill_value = round(item['total_bill_value'])
        total_pay_sum = round(item['TIEN_TIEPKHACH'])
        pos_close_transaction_time = item['pos_close_transaction_time']
        ten_nhahang = item['name']

        chuoi_html_danh_sach_tiep_khach += '''
        <tr>
          <th width="200">'''+name_on_pos+'''</th>
          <th width="150">'''+str(clm_card_no)+'''</th>
          <th width="70">'''+str(clm_mem_id)+'''</th>
          <th width="70">'''+str(check_number)+'''</th>
          <th width="100">{:,}'''.format(total_bill_value).replace(",", ".")+'''</th>
          <th width="100">{:,}'''.format(total_pay_sum).replace(",", ".")+'''</th>
          <th width="100">'''+str(pos_close_transaction_time)+'''</th>
          <th width="100">'''+ten_nhahang+'''</th>
          </tr>
        '''

    conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Báo Cáo Chi Tiết Theo Ngày  End ===============================
# =================




# =============================== Báo Cáo Tiếp Khách Số Dư CÁ NHÂN USER Start ===============================
def BAO_CAO_TIEP_KHACH_SO_DU_CA_NHAN_USER(user_ca_nhan_1):
    chuoi_html_danh_sach_tiep_khach = 'Nhân Viên Này Chưa Được Khai Báo Mã Nhân Viên'
    connection = connect_database()
    if user_ca_nhan_1 !='0':
        chuoi_html_danh_sach_tiep_khach = ''
        conn = connection.cursor()
        sql = 'SELECT A.name_on_pos,B.year,B.month,B.granted_amount,B.amount , (B.granted_amount - B.amount) AS "CON_LAI" \
                    from staff_monthly_credits AS B , staff_credits AS A \
                    where YEAR(NOW()) = B.year AND B.clm_mem_id =  A.clm_mem_id AND A.name_on_pos LIKE %s\
                    ORDER BY A.clm_mem_id , B.month  DESC LIMIT 2'
        user_ca_nhan = '%'+str(user_ca_nhan_1)+'%'
        conn.execute(sql,str(user_ca_nhan))
        danh_sach = conn.fetchall()
        for item in danh_sach:
            # print(item['clm_mem_id'])

            name_on_pos = item['name_on_pos']
            year = item['year']
            month = item['month']
            han_muc = round(item['granted_amount'])
            da_dung = round(item['amount'])
            CON_LAI = round(item['CON_LAI'])

            chuoi_html_danh_sach_tiep_khach += '''
                    <tr>
              <th width="240">'''+name_on_pos+'''</th>
              <th width="100">'''+str(year)+'''/'''+str(month)+'''</th>
              <th width="100">{:,}'''.format(han_muc).replace(",", ".")+'''</th>
              <th width="100">{:,}'''.format(da_dung).replace(",", ".")+'''</th>
              <th width="100">{:,}'''.format(CON_LAI).replace(",", ".")+'''</th>
            </tr>
            '''

        conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Báo Cáo Tiếp Khách Số Dư CÁ NHÂN USER End ===============================
# =================





# =============================== Báo Cáo Chi Tiết Tiếp Khách CÁ NHÂN USER Start ===============================
def BAO_CAO_TIEP_KHACH_CHI_TIET_CA_NHAN_USER(clm_mem_id):
    chuoi_html_danh_sach_tiep_khach = ''
    connection = connect_database()
    conn = connection.cursor()
    sql = 'SELECT D.name_on_pos,D.clm_card_no,D.clm_mem_id,A.check_number,A.total_bill_value,E.amount AS "TIEN_TIEPKHACH", \
            A.total_pay_sum,A.pos_close_transaction_time,B.name \
            FROM pos_transactions AS A  \
            INNER JOIN restaurants AS B ON A.restaurant_code = B.code \
						INNER JOIN staff_credits AS D ON A.clm_mem_id = D.clm_mem_id \
            INNER JOIN pos_transaction_payment_details AS E ON A.id = E.transaction_id \
            where \
						YEAR(NOW()) = YEAR(A.create_time) \
            AND D.clm_mem_id = %s \
            AND E.rk_payment_code = "390" \
            ORDER BY D.clm_mem_id,A.pos_close_transaction_time DESC LIMIT 30'
    memid = clm_mem_id
    conn.execute(sql,str(memid))
    danh_sach = conn.fetchall()
    for item in danh_sach:
        # print(item['clm_mem_id'])

        name_on_pos = item['name_on_pos']
        clm_card_no = item['clm_card_no']
        clm_mem_id = item['clm_mem_id']
        check_number = item['check_number']
        total_bill_value = round(item['total_bill_value'])
        total_pay_sum = round(item['total_pay_sum'])
        tien_tiep_khach = round(item['TIEN_TIEPKHACH'])
        pos_close_transaction_time = item['pos_close_transaction_time']
        ten_nhahang = item['name']

        chuoi_html_danh_sach_tiep_khach += '''
        <tr>
          <th width="200">'''+name_on_pos+'''</th>
          <th width="70">'''+str(check_number)+'''</th>
          <th width="100">{:,}'''.format(total_bill_value).replace(",", ".")+'''</th>
          <th width="100">{:,}'''.format(tien_tiep_khach).replace(",", ".")+'''</th>
          <th width="100">'''+str(pos_close_transaction_time)+'''</th>
          <th width="100">'''+ten_nhahang+'''</th>
          </tr>
        '''

    conn.close()
    return Markup(chuoi_html_danh_sach_tiep_khach)
# =============================== Báo Cáo Chi Tiết Tiếp Khách CÁ NHÂN USER End ===============================
# =================





# =============================== Check Memid CÁ NHÂN USER qua Mã Nhân Viên Start ===============================
def Check_Memid_tu_Ma_NV(manv):
    connection = connect_database()
    clm_mem_id = ''
    conn = connection.cursor()
    sql = 'SELECT clm_mem_id FROM staff_credits where name_on_pos LIKE %s LIMIT 1'
    ma_nhan_vien = '%'+str(manv)+'%'
    conn.execute(sql,str(ma_nhan_vien))
    danh_sach = conn.fetchall()
    for item in danh_sach:
        clm_mem_id = item['clm_mem_id']
    conn.close()
    return clm_mem_id
# =============================== Check Memid CÁ NHÂN USER qua Mã Nhân Viên Start ===============================
# =================




# ================================ Strat danh sách nhân viên Nhân Sự HR =================================
def Chuoi_HTML_DANH_SACH_NHAN_VIEN_USER_HR():
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT * FROM NHAN_VIEN_GGG ORDER BY ngay_chinh_sua DESC LIMIT 100"
    ket_qua = conn.execute(chuoi_sql)
    chuoi_html_check_nhan_vien = '<h2 class="font-weight-bold" style="text-align:center;">Không Có Nhân Viên Nào</h2>'
    # print(ket_qua)
    if ket_qua is not None:
        chuoi_html_check_nhan_vien =''
        for list1 in ket_qua:
            _id = list1[0]
            ma_nhanvien = list1[1]
            ho_ten = list1[2]
            cmnd = list1[3]
            don_vi = list1[4]
            bo_phan = list1[5]
            cap_bac = list1[6]
            tinh_trang = list1[7]
            color  = 'green'
            if tinh_trang == "On":
                tinh_trang = "Còn Làm Việc"
                color = 'green'
            else:
                tinh_trang = "Đã Nghỉ Việc"
                color = 'red'
            
            chuoi_html_check_nhan_vien +='''            
                                        <tr>
                  <th style="width:9%">'''+ma_nhanvien+'''</th>
                  <th style="width:20%">'''+ho_ten+'''</th>
                  <th style="width:10%">'''+cmnd+'''</th>
                  <th style="width:7%"; color :'''+color+''';"><b>'''+cap_bac+'''</b></th>
                  <th style="width:10% ;color :'''+color+''';"><b>'''+tinh_trang+'''</b></th>
                  <th style="width:12%">'''+don_vi+'''</th>
                  <th style="width:15%">'''+bo_phan+'''</th>
                  <th style="width:10%">
                      <a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>
                  </th>
                </tr>   


                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update Thông Tin Nhân Viên GGG</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                      <input name="manv_update" type="text" class="form-control" id="recipient-name" value="'''+ma_nhanvien+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Họ Tên:(*)</label>
                      <input name="ho_ten_update" type="text" class="form-control" id="recipient-name"value="'''+ho_ten+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Chứng Minh Nhân Dân:(*)</label>
                      <input name="cmnd_update" type="text" class="form-control" id="recipient-name" value="'''+cmnd+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Cấp Bậc:(*)</label>
                      <input name="cap_bac_update" type="text" class="form-control" id="recipient-name"  value="'''+cap_bac+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Đơn Vị:(*)</label>
                      <input name="don_vi_update" type="text" class="form-control" id="recipient-name" value="'''+don_vi+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Bộ Phận:(*)</label>
                      <input name="bo_phan_update" type="text" class="form-control" id="recipient-name" value="'''+bo_phan+'''" required>
                    </div>

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Trạng Thái:(*)</label>
                            <div class="form-group">
                              <select name="tinh_trang_update" class="form-control">
                                <option label="Còn Làm Việc">On</option>
                                <option label="Đã Nghỉ Việc">NO</option>
                              </select>
                            </div>
                            </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>
                <!--Modal: modalConfirm UPDATE-->
                </form>
                  </div>
                      '''

    conn.close()
    return Markup(chuoi_html_check_nhan_vien)
# ================================ END danh sách nhân viên Nhân Sự HR =================================
# =============


# ================================ Strat danh sách nhân viên Nhân Sự THEO LOAD USER HR=================================
def Chuoi_HTML_DANH_SACH_NHAN_VIEN_THEO_LOAD_USER_HR(load_nhan_vien):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT * FROM NHAN_VIEN_GGG ORDER BY ngay_chinh_sua DESC LIMIT ? "
    ket_qua = conn.execute(chuoi_sql,(int(load_nhan_vien),))
    chuoi_html_check_nhan_vien = '<h2 class="font-weight-bold" style="text-align:center;">Không Có Nhân Viên Nào</h2>'
    # print(ket_qua)
    if ket_qua is not None:
        chuoi_html_check_nhan_vien =''
        for list1 in ket_qua:
            _id = list1[0]
            ma_nhanvien = list1[1]
            ho_ten = list1[2]
            cmnd = list1[3]
            don_vi = list1[4]
            bo_phan = list1[5]
            cap_bac = list1[6]
            tinh_trang = list1[7]
            color  = 'green'
            if tinh_trang == "On":
                tinh_trang = "Còn Làm Việc"
                color = 'green'
            else:
                tinh_trang = "Đã Nghỉ Việc"
                color = 'red'
            
         
            chuoi_html_check_nhan_vien +='''            
                                        <tr>
                  <th style="width:9%">'''+ma_nhanvien+'''</th>
                  <th style="width:20%">'''+ho_ten+'''</th>
                  <th style="width:10%">'''+cmnd+'''</th>
                  <th style="width:7%"; color :'''+color+''';"><b>'''+cap_bac+'''</b></th>
                  <th style="width:10% ;color :'''+color+''';"><b>'''+tinh_trang+'''</b></th>
                  <th style="width:12%">'''+don_vi+'''</th>
                  <th style="width:15%">'''+bo_phan+'''</th>
                  <th style="width:10%">
                      <a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>
                  </th>
                </tr>   


                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update Thông Tin Nhân Viên GGG</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                      <input name="manv_update" type="text" class="form-control" id="recipient-name" value="'''+ma_nhanvien+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Họ Tên:(*)</label>
                      <input name="ho_ten_update" type="text" class="form-control" id="recipient-name" value="'''+ho_ten+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Chứng Minh Nhân Dân:(*)</label>
                      <input name="cmnd_update" type="text" class="form-control" id="recipient-name" value="'''+cmnd+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Cấp Bậc:(*)</label>
                      <input name="cap_bac_update" type="text" class="form-control" id="recipient-name"  value="'''+cap_bac+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Đơn Vị:(*)</label>
                      <input name="don_vi_update" type="text" class="form-control" id="recipient-name"  value="'''+don_vi+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Bộ Phận:(*)</label>
                      <input name="bo_phan_update" type="text" class="form-control" id="recipient-name"  value="'''+bo_phan+'''" required>
                    </div>

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Trạng Thái:(*)</label>
                            <div class="form-group">
                              <select name="tinh_trang_update" class="form-control">
                                <option label="Còn Làm Việc">On</option>
                                <option label="Đã Nghỉ Việc">NO</option>
                              </select>
                            </div>
                            </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>
                <!--Modal: modalConfirm UPDATE-->
                </form>
                  </div>
                      '''
    conn.close()
    return Markup(chuoi_html_check_nhan_vien)
# ================================ END danh sách nhân viên Nhân Sự THEO LOAD USER HR =================================
# =============




# ================================ Strat danh sách nhân viên Nhân Sự HR TIM KIEM =================================
def Chuoi_HTML_DANH_SACH_NHAN_VIEN_USER_HR_TIM_KIEM(MA_NHAN_VIEN):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT id,ma_nhanvien,ho_ten,cmnd,don_vi,bo_phan,cap_bac,tinh_trang FROM NHAN_VIEN_GGG where ma_nhanvien = ? OR cmnd = ? LIMIT 3"
    ket_qua = conn.execute(chuoi_sql,(MA_NHAN_VIEN,MA_NHAN_VIEN))
    chuoi_html_check_nhan_vien = '<h2 class="font-weight-bold" style="text-align:center;">Không Có Nhân Viên Nào</h2>'
    # print(ket_qua)
    if ket_qua is not None:
        chuoi_html_check_nhan_vien =''
        for list1 in ket_qua:
            _id = list1[0]
            ma_nhanvien = list1[1]
            ho_ten = list1[2]
            cmnd = list1[3]
            don_vi = list1[4]
            bo_phan = list1[5]
            cap_bac = list1[6]
            tinh_trang = list1[7]
            color  = 'green'
            if tinh_trang == "On":
                tinh_trang = "Còn Làm Việc"
                color = 'green'
            else:
                tinh_trang = "Đã Nghỉ Việc"
                color = 'red'
            
            chuoi_html_check_nhan_vien +='''            
                                        <tr>
                  <th style="width:9%">'''+ma_nhanvien+'''</th>
                  <th style="width:20%">'''+ho_ten+'''</th>
                  <th style="width:10%">'''+cmnd+'''</th>
                  <th style="width:7%"; color :'''+color+''';"><b>'''+cap_bac+'''</b></th>
                  <th style="width:10% ;color :'''+color+''';"><b>'''+tinh_trang+'''</b></th>
                  <th style="width:12%">'''+don_vi+'''</th>
                  <th style="width:15%">'''+bo_phan+'''</th>
                  <th style="width:10%">
                      <a style="background-color: #FFCC00;" class="btn btn-danger" data-toggle="modal"
                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>
                  </th>
                </tr>   


                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update Thông Tin Nhân Viên GGG</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Mã Nhân Viên:(*)</label>
                      <input name="manv_update" type="text" class="form-control" id="recipient-name" value="'''+ma_nhanvien+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">                                       
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Họ Tên:(*)</label>
                      <input name="ho_ten_update" type="text" class="form-control" id="recipient-name"value="'''+ho_ten+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Chứng Minh Nhân Dân:(*)</label>
                      <input name="cmnd_update" type="text" class="form-control" id="recipient-name" value="'''+cmnd+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Cấp Bậc:(*)</label>
                      <input name="cap_bac_update" type="text" class="form-control" id="recipient-name"  value="'''+cap_bac+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Đơn Vị:(*)</label>
                      <input name="don_vi_update" type="text" class="form-control" id="recipient-name" value="'''+don_vi+'''" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Bộ Phận:(*)</label>
                      <input name="bo_phan_update" type="text" class="form-control" id="recipient-name" value="'''+bo_phan+'''" required>
                    </div>

                          <div class="form-group">
                            <label for="recipient-name" class="col-form-label">Trạng Thái:(*)</label>
                            <div class="form-group">
                              <select name="tinh_trang_update" class="form-control">
                                <option label="Còn Làm Việc">On</option>
                                <option label="Đã Nghỉ Việc">NO</option>
                              </select>
                            </div>
                            </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>
                <!--Modal: modalConfirm UPDATE-->
                </form>
                  </div>
                      '''

    conn.close()
    return Markup(chuoi_html_check_nhan_vien)
# ================================ END danh sách nhân viên Nhân Sự TIM KIEM HR =================================
# =============




# =============================== Check-Insert Nhân Viên Start ===============================
def CHECK_INSERT_HR_GGG(ma_nv,cmnd):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT id FROM NHAN_VIEN_GGG where ma_nhanvien = ? OR cmnd = ? LIMIT 1"
    ket_qua = conn.execute(chuoi_sql,(ma_nv,cmnd))
    list_dang_nhap = '-1'
    if ket_qua is not None:
        for ten in ket_qua:
            list_dang_nhap = ten[0]
        # print(list_dang_nhap)
    conn.close()
    return list_dang_nhap
# =============================== Check-Insert Nhân Viên END ===============================
# =================






# =============================== Danh sách Nhân Viên Nhà Hàng Start ===============================
def Chuoi_HTML_TIM_KIEM_NHAN_VIEN(check_nhan_vien):
    conn = sqlite3.connect("South_File_Managerment/DB/GGG.db", check_same_thread=False)
    chuoi_sql = "SELECT * FROM NHAN_VIEN_GGG WHERE ma_nhanvien =? OR cmnd =? AND ACTIVE = '1' LIMIT 2"
    ket_qua = conn.execute(chuoi_sql, (check_nhan_vien, check_nhan_vien))
    hop_le = '1'
    chuoi_html_check_nhan_vien = '<h2 class="font-weight-bold" style="text-align:center;">Không Có Thông Tin Nhân Viên " '+check_nhan_vien+' "  </h2>'
    # print(ket_qua)
    if ket_qua is not None:
        hop_le = '2'
        for list1 in ket_qua:
            ma_nhanvien = list1[1]
            ho_ten = list1[2]
            cmnd = list1[3]
            don_vi = list1[4]
            bo_phan = list1[5]
            cap_bac = list1[6]
            tinh_trang = list1[7]
            if tinh_trang == "On":
                tinh_trang = "Còn Làm Việc"
            else:
                tinh_trang = "Đã Nghỉ Việc"
            
            chuoi_html_check_nhan_vien='''            

                        <table class="table table-bordered">
                            <thead>
                              <tr>
                                <th scope="col">Mã Nhân Viên</th>
                                <th scope="col">Tình Trạng</th>
                                <th scope="col">Họ Tên Nhân Viên</th>
                                <th scope="col">Cấp Bậc</th>
                                <th scope="col">Chứng Minh Nhân Dân</th>
                                <th scope="col">Đơn Vị</th>
                                <th scope="col">Bộ Phận</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <th scope="row">'''+ma_nhanvien+'''</th>
                                <td style ="color :red;"><b>'''+tinh_trang+'''</b></td>
                                <td>'''+ho_ten+'''</td>
                                <td style ="color :red;"><b>'''+cap_bac+'''</b></td>
                                <td>'''+cmnd+'''</td>
                                <td>'''+don_vi+'''</td>
                                <td>'''+bo_phan+'''</td>
                              </tr>
                            </tbody>
                          </table>                   
                  '''

    return Markup(chuoi_html_check_nhan_vien)

# =============================== Danh sách Nhân Viên Nhà Hàng END ===============================
# ===============






# =============================== Báo Cáo Upload File Start ===============================
def CHUOI_HTML_DANH_SACH_FILE_BAO_CAO_ADMIN():
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = 'SELECT TOP 100 id,ten_chung_tu,data,ngay_can_thong_bao,ghi_chu,user_them,user_update,ngay_them,\
      ten_file_luu,thong_bao,active FROM UPLOAD_FILE_MANAGERMENT ORDER BY ngay_them DESC'
    conn_2014.execute(sql)  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ten_file_luu = item[8]
            thong_bao = item[9]
            active = item[10]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data">
                                    <div class="form-group col-md-4">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <div class="row" >
                                      <div class="col-md-8">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ngày Thêm : '''+str(ngay_them)+''' </h8><br>
                                        <h8 align="left">User : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">Trạng Thái : '''+str(active)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      <div class="col-md-3">
                                        <button type="submit" style="background-color:#DAA520; color:black" >Dowload</button><br>
                                        <a href="#">Update</a>
                                      </div>
                                      </div>
                                    --------------------------------------------------
                                      </div>
                                  </form>
                                '''
    return Markup(list_danh_sach)

# =============================== Báo Cáo Upload File End ===============================
# =============







# =============================== Check Món Đã Được Đẩy Từ SAP Xuống RK7 Chưa Start ===============================
def CHUOI_HTML_CHECK_MON_DA_DUOC_DAY_TU_SAP_XUONG_CHUA(list_mon):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014_Dcorp()
    conn_2014 = connection_2014.cursor()
    # print(conn_2014)
    sql = "SELECT\
            BANG_CHUA_SAP_CODE.PROPERTYVAL AS 'SAPCODE'\
            ,MENU.NAME AS 'TÊN MÓN'\
            ,MENU.SIFR AS 'RK7 IDENT'\
            ,MENU.CODE AS 'RK7 CODE'\
            ,GIA_TIEN.VALUE AS 'Giá Tiền'\
            ,TEN_DON_GIA.NAME AS 'TÊN ĐƠN GIÁ RK7'\
            ,MENU.PORTIONNAME AS 'Đơn Vị Tính'\
            ,SELECTOR.NAME\
            FROM dbo.MENUITEMS AS MENU\
            LEFT JOIN GENERATEDPROPDATAS AS BANG_CHUA_SAP_CODE ON BANG_CHUA_SAP_CODE.OBJECTIDENT = MENU.SIFR\
            LEFT JOIN dbo.PRICES AS GIA_TIEN ON GIA_TIEN.OBJECTID = MENU.SIFR\
            LEFT JOIN dbo.PRICETYPES AS TEN_DON_GIA ON TEN_DON_GIA.SIFR = GIA_TIEN.PRICETYPE\
            LEFT JOIN CATEGLIST AS SELECTOR ON SELECTOR.SIFR=MENU.PARENT\
            WHERE 1=1\
            AND BANG_CHUA_SAP_CODE.PROPERTYVAL IN (?)"
    conn_2014.execute(sql,(list_mon,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            SAPCODE = item[0]
            TEN = item[1]
            list_danh_sach += TEN

    return Markup(list_danh_sach)
# =============================== Check Món Đã Được Đẩy Từ SAP Xuống RK7 Chưa END ===============================
# =================





# =============================== Báo Cáo Lưu File USER Start ===============================
def CHUOI_HTML_BAO_CAO_LUU_FILE_USER(USER):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT TOP 50 * FROM UPLOAD_FILE_MANAGERMENT WHERE user_them = ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(USER))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Báo Cáo Lưu File USER End ===============================
# =============





# =============================== Tìm Kiếm Báo Cáo Lưu File USER Start ===============================
def CHUOI_HTML_TIM_KIEM_BAO_CAO_LUU_FILE_USER(USER,TIM_KIEM):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT * FROM UPLOAD_FILE_MANAGERMENT WHERE user_them = ? AND ten_chung_tu LIKE ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(USER,TIM_KIEM,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Tìm Kiếm Báo Cáo Lưu File USER End ===============================
# =============



# =============================== Tìm Kiếm Theo Ngày Báo Cáo Lưu File USER Start ===============================
def CHUOI_HTML_TIM_KIEM_THEO_NGAY_BAO_CAO_LUU_FILE_USER(USER,TU_NGAY,DEN_NGAY):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT * FROM UPLOAD_FILE_MANAGERMENT WHERE user_them = ? AND ngay_het_han >= ? AND ngay_het_han <=?  ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(USER,TU_NGAY,DEN_NGAY,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Tìm Kiếm Theo Ngày Báo Cáo Lưu File USER End ===============================
# =============




# =============================== Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_BAO_CAO_LUU_FILE_TRUONG_PHONG(phong_ban):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT TOP 50 * FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(phong_ban))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Báo Cáo Lưu File TRƯỞNG PHÒNG End ===============================
# =============





# =============================== Tìm Kiếm Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_TIM_KIEM_BAO_CAO_LUU_FILE_TRUONG_PHONG(phong_ban,TIM_KIEM):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT * FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? AND ten_chung_tu LIKE ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(phong_ban,TIM_KIEM,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Tìm Kiếm Báo Cáo Lưu File TRƯỞNG PHÒNG End ===============================
# =============




# =============================== Tìm Kiếm Theo Ngày Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_TIM_KIEM_THEO_NGAY_BAO_CAO_LUU_FILE_TRUONG_PHONG(phong_ban,TU_NGAY,DEN_NGAY):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT * FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? AND ngay_het_han >= ? AND ngay_het_han <=?  ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(phong_ban,TU_NGAY,DEN_NGAY,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Tìm Kiếm Theo Ngày Báo Cáo Lưu File TRƯỞNG PHÒNG End ===============================
# =============






# =============================== JOB Tự Động Gửi Mail START ===============================
# =================
# def JOB_GUI_MAIL():
#     ngay_hien_tai = datetime.datetime.now()
#     ngay_hien_tai_1 = ngay_hien_tai.strftime("%Y-%m-%d")   

#     connection_2014 = connect_database_SQL_2014()
#     conn_2014 = connection_2014.cursor()
#     sql = 'SELECT top 1 user_them,ten_chung_tu FROM UPLOAD_FILE_MANAGERMENT WHERE ngay_het_han = ? AND thong_bao="1" '
#     conn_2014.execute(sql)  
#     danh_sach = conn_2014.fetchall()   
#     list_danh_sach = ['-1', '-1']
#     if danh_sach is not None:
#         for item in danh_sach:
#             list_danh_sach.clear()
#             list_danh_sach.append(str(item[0]))
#             list_danh_sach.append(item[1])
#         # print(list_danh_sach)
#     conn_2014.close()
#     return list_danh_sach
# =============================== JOB Tự Động Gửi Mail END ===============================
# =================






# =============================== Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_BAO_CAO_LUU_FILE_ADMIN(phong_ban):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT TOP 100 * FROM UPLOAD_FILE_MANAGERMENT WHERE phong_ban = ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(phong_ban))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Báo Cáo Lưu File TRƯỞNG PHÒNG End ===============================
# =============




# =============================== Tìm Kiếm Báo Cáo Lưu File TRƯỞNG PHÒNG Start ===============================
def CHUOI_HTML_TIM_KIEM_BAO_CAO_LUU_FILE_ADMIN(TIM_KIEM):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    conn_2014 = connection_2014.cursor()
    # print(USER)
    sql = 'SELECT * FROM UPLOAD_FILE_MANAGERMENT WHERE ten_chung_tu LIKE ? ORDER BY ngay_them DESC'
    conn_2014.execute(sql,(TIM_KIEM,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
            _id = item[0]
            ten_chung_tu = item[1]
            data = item[2]
            ngay_can_thong_bao = item[3]
            ghi_chu = item[4]
            user_them = item[5]
            user_update = item[6]
            ngay_them = item[7]
            ngay_update = item[8]
            ten_file_luu = item[9]
            thong_bao = item[10]
            if thong_bao == 1 :
              check = 'checked="checked"'
            else:
              check=''
            active = item[11]
            if active == 1:
              active='Hoạt Động'
            else:
              active='Đã Xóa'
            ngay_het_han = item[12]
            s2 = ngay_het_han.strftime("%Y-%m-%d") 
            s3 = ngay_can_thong_bao.strftime("%Y-%m-%d") 
            list_danh_sach +='''
                                    <form method="POST" enctype="multipart/form-data" >
                                    <div class="form-group col-md-4" style="border: thin solid yellow">
                                      <h5>'''+str(ten_chung_tu)+'''</h5>
                                      <h8>Ngày Hết Hạn : '''+str(s2)+''' </h8><br>
                                      <a align="left" data-toggle="collapse" href="#test'''+str(_id)+'''" role="button" style="color:red"> Xem Chi Tiết...</a>
                                      <div class="row collapse multi-collapse" id="test'''+str(_id)+'''">
                                      <div class="col-md-12">
                                        <input type="hidden" name="id_dowload" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                                        <h8 align="left">Ghi Chú : '''+str(ghi_chu)+''' </h8><br>
                                        <h8 align="left">User Thêm : '''+str(user_them)+''' </h8><br>
                                        <h8 align="left">'''+str(ten_file_luu)+'''</h8>
                                      </div>
                                      </div>  

                                      <div style="text-align:center;" class="collapse multi-collapse" id="test'''+str(_id)+'''" >
                                      <button class="btn btn-danger" type="submit" style="background-color:#DAA520; color:black" >Dowload</button>
                                      <a style="background-color: #DAA520;" class="btn btn-danger" data-toggle="modal"
                                      data-target="#UPDATE'''+str(_id)+'''" data-toggle="modal"> UPDATE </a>                                      
                                      </div> 
                                      </div>
                                  </form>



                  <!--Modal: modalConfirm UPDATE-->
          <div class="modal fade" id="UPDATE'''+str(_id)+'''" data-backdrop="static" tabindex="-1" role="dialog"
            aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">

                <div class="modal-header" style="text-align:center;">
                  <h5 class="modal-title" id="exampleModalLabel">Update File Lưu Trữ Tập Chung</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <form method="POST" enctype="multipart/form-data">

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Tên Chứng Từ:(*)</label>
                      <input name="ten_chung_tu_update" type="text" class="form-control" id="recipient-name" value="'''+str(ten_chung_tu)+'''" required>
                      <input type="hidden" name="txt_id_update" style="height:0px;width:0px;" value="'''+str(_id)+'''">
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Ghi Chú : </label>
                      <textarea name="ghi_chu_update" rows="5" cols="61" placeholder="Ghi Chú Thêm">'''+str(ghi_chu)+'''</textarea>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">	Ngày Hết Hạn:(*)</label>
                       <input class="form-control" name="ngay_het_han_update" max ="2050-12-01" min ="2000-12-01" value="'''+str(s2)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                      <label for="recipient-name" class="col-form-label">Check Để Nhận Thông Báo</label>
                      <input name = "check_thong_bao_update" type="checkbox" value="1" '''+check+'''>
                      <input class="form-control" max ="2050-12-01" min ="2000-12-01" name="ngay_thong_bao_update" value="'''+str(s3)+'''" type="date" required>
                    </div>

                    <div class="form-group">
                    <input type="file" name="file_upload"class="form-control-file">
                    File Sẵn Có : '''+str(ten_file_luu)+'''
                    </div>


                      <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

                      </div>

                        </form>
                      </div>

                    </div>
                  </div>
                </div>

                                '''





    return Markup(list_danh_sach)

# =============================== Tìm Kiếm Báo Cáo Lưu File TRƯỞNG PHÒNG End ===============================
# =============

