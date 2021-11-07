from flask_wtf import Form, FlaskForm
from wtforms import TextField,StringField,IntegerField,TextField, TextAreaField, SubmitField, validators, ValidationError,PasswordField, RadioField,SelectField,FileField
from flask_wtf.file import FileAllowed
from flask_ckeditor import CKEditorField


class Form_update(FlaskForm):
    Th_Hinhdinhkem = FileField("")
    Th_Nhom_mon = SelectField("Nhóm Món", choices=[('1','THỊT HẢO HẠNG (1)'),
                        ('2','Hải Sản + Lẩu + Cơm + Canh (2)'),('3','Rau Mì Nấm (3)')],
                        default='1')