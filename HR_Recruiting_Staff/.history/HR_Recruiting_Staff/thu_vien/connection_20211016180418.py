from flask import render_template , request , Markup , url_for , redirect , session, sessions
import os
from HR_Recruiting_Staff import app
from datetime import datetime
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
import pyodbc



# def connect_database():
#     connection = pymysql.connect(host='10.28.1.78',
#                              user='dung.nguyenanh',
#                              password='q123456',                             
#                              db='paymenthub.ggg.com.vn',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
 
#     a = "connect successful!!"
#     return connection



def connect_database_SQL_2014():
    server = '172.16.8.43' 
    database = 'HR_Recruiting_Staff' 
    username = 'webtuyendung' 
    password = 'A@12345677' 

    try:
  
        cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  # Perform database operations

    except pyodbc.Error as err:
        print('fail 1')
    except pyodbc.OperationalError as err:
        print('fail 2 ')
    except pyodbc.DataError as err:
        print('fail.......3..............')
    except pyodbc.IntegrityError as err:
        print('fail........4.............')
    except pyodbc.ProgrammingError as err:
        print('fail........5.............')
    except pyodbc.NotSupportedError as err:
        print('fail.........6............')
    except pyodbc.DatabaseError as err:
        print('fail.........7............')
    except pyodbc.Error as err:
        print('fail.....................')

    return cnxn




# def connect_database_SQL_2014_Dcorp():
#     server = '10.21.1.4' 
#     database = 'GGGHCMREPH_PROD' 
#     username = 'dung.nguyenanh' 
#     password = 'Ggg@)@!' 
#     cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#     return cnxn