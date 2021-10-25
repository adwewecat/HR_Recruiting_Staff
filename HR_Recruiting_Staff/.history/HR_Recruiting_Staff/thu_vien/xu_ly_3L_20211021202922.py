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





# =============================== Trang nhà hàng bản tin còn sử dụng Start ===============================
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
                                            Số Lượng Người Thực Tế Tuyển Được
                                              <input class="nha_hang_bantin_new__soluong-thuc-item" type="number" min="1" name="so_luong_thuc_te" id="so_luong_thuc_te"
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
# =============================== Trang nhà hàng bản tin còn sử dụng END ===============================
# =================





# =============================== Trang nhà hàng bản tin hoàn thành Start ===============================
def CHUOI_HTML_NHA_HANG_BAN_TIN_HOAN_THANH(restaurant_id):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = "SELECT\
              id,\
              note,\
              staff_quantity_thucte,\
              FORMAT(time_from, 'hh') AS h_timefrom,\
              FORMAT(time_from, 'mm') AS m_timefrom,\
              FORMAT(time_to, 'hh') AS h_timeto,\
              FORMAT(time_to, 'mm') AS m_timeto\
              FROM [dbo].[Newpost]\
              WHERE\
              restaurant_id = ?\
              AND active = 0\
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
                                    <div class="nha_hang_danh_sach__new-item"'''+str(ID)+'''">
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
                                    </div>
                                  </div>
                                  
                              '''   
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang nhà hàng bản tin hoàn thành END ===============================
# =================








# =============================== Trang Nhà Hàng Thông Tin Start ===============================
def CHUOI_HTML_NHA_HANG_THONG_TIN(id_nha_hang):
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = 'select top 1 name,address,sdt from [dbo].[Restaurants] where id= ? '
      conn_2014.execute(sql,id_nha_hang)  
      danh_sach = conn_2014.fetchall()   
      if danh_sach is not None:
          for item in danh_sach:
              NAME = item[0]
              DIA_CHI = item[1]
              SDT = item[2]
              list_danh_sach +='''
                                <div class="nha_hang_thongtin-chitiet">
                                <div class="nha_hang_thongtin-chitiet__list">
                                  <div class="nha_hang_thongtin-chitiet__item">
                                    <span class="nha_hang_thongtin-chitiet__item-item">Nhà Hàng : </span>
                                    '''+str(NAME)+'''
                                  </div>

                                  <div class="nha_hang_thongtin-chitiet__item">
                                    <span class="nha_hang_thongtin-chitiet__item-item">Số điện thoại : </span>
                                    '''+str(SDT)+'''
                                  </div>

                                  <div class="nha_hang_thongtin-chitiet__item">
                                    <span class="nha_hang_thongtin-chitiet__item-item">Địa Chỉ : </span>
                                    '''+str(DIA_CHI)+'''
                                  </div>

                                </div>
                              </div>
                              '''   
    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Nhà Hàng Thông Tin END ===============================
# =================




# =============================== XỬ LÝ ĐĂNG NHẬP START ===============================
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
# =============================== XỬ LÝ ĐĂNG NHẬP END=============================
# =================






# =============================== GET THONG TIN NHÀ HÀNG START ===============================
# =================
def GET_THONG_TIN_NHAHANG(id_nha_hang):
    list_dang_nhap = [ '-1','-1','-1']
    connection_2014 = connect_database_SQL_2014()

    conn_2014 = connection_2014.cursor()
    sql = "select TOP 1 brand,district,Regions_name from [dbo].[Restaurants] where id=?"
    conn_2014.execute(sql,(id_nha_hang,))  
    danh_sach = conn_2014.fetchall()   
    if danh_sach is not None:
        for item in danh_sach:
          list_dang_nhap.clear()
          list_dang_nhap.append(item[0])
          list_dang_nhap.append(item[1])
          list_dang_nhap.append(item[2])
    return list_dang_nhap
# =============================== GET THONG TIN NHÀ HÀNG END ===============================
# =================






# =============================== GET THONG TIN Đăng Xuất START ===============================
# =================
def GET_THONG_TIN_DANG_XUAT(phan_quyen,id_nha_hang,full_name,user_name):
    danh_sach = ''
    if phan_quyen =='nhahang':
      phan_quyen='Nhà Hàng'
    danh_sach += '''
                      <!-- Modal -->
              <div class="modal fade" id="DANGXUAT" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered dialog_dangxuat" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="exampleModalLongTitle">Thông Tin Tài Khoản</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-body modal-body__dangxuat">
                      <form method="POST" enctype="multipart/form-data">
                        <div class="form-group form-group__dangxuat">
                          <label for="user-name" class="col-form-label">Tên Nhà Hàng : </label>
                          <span>'''+str(full_name)+'''</span>
                        </div>
                        <div class="form-group form-group__dangxuat">
                          <label for="user-name" class="col-form-label">User Đăng Nhập : </label>
                          <span>'''+str(user_name)+'''</span>
                        </div>
                          <div class="form-group form-group__dangxuat">
                          <label for="user-name" class="col-form-label">ID Nhà Hàng : </label>
                          <span>'''+str(id_nha_hang)+'''</span>
                        </div>
                          <div class="form-group form-group__dangxuat">
                          <label for="user-name" class="col-form-label">Phân Quyền : </label>
                          <span>'''+str(phan_quyen)+'''</span>
                        </div>
                    </div>
                    <div class="modal-footer modal-footer__dang_xuat">
                      <button type="button" class="btn btn-secondary" data-dismiss="modal">
                        Close
                      </button>
                      <a href="/dang-xuat" class="button__dang-tin-item btn__dangxuat">Đăng Xuất</a>
                    </div>
                    </form>
                  </div>
                </div>
              </div>
    
                  '''

          
    return Markup(danh_sach)
# =============================== GET THONG TIN Đăng Xuất END ===============================
# =================








# =============================== INSERT BẢN TIN NHÀ HÀNG Start ===============================
def INSERT_BAN_TIN_NHA_HANG():
    list_danh_sach =''
    connection_2014 = connect_database_SQL_2014()
    if connection_2014 != '1':
      conn_2014 = connection_2014.cursor()
      sql = "INSERT INTO Newpost\
                (\
                restaurant_id,\
                brand_id,\
                district_id,\
                region_id,\
                note,\
                time_from,\
                time_to,\
                staff_quantity,\
                user_dang_bai,\
                active\
                )\
                VALUES \
                (\
                ?,?,?,?,?,?,?,?,?,'1'\
                )\
            "
      conn_2014.execute(sql)  
      conn_2014.commit()
      conn_2014.close()


    else:
        list_danh_sach =' <h1> Lỗi Kết Nối Đến Server <h1>'
    return Markup(list_danh_sach)
# =============================== Trang Index Brand END ===============================
# =================
























