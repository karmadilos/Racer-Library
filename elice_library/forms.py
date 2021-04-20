from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('이름은 필수 입력 항목입니다.'), Length(min=2, max=25), Regexp("^[가-힣]+$|^[a-zA-Z]+\s?[a-zA-Z]+$", message="한글 또는 영어만 입력가능합니다.")])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.'), Regexp("^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{10,}$|^(?=.*[a-zA-Z])(?=.*[!@#$%^&*?])[a-zA-Z!@#$%^&*?]{10,}$|^(?=.*[!@#$%^&*?])(?=.*[0-9])[!@#$%^&*?0-9]{10,}$|^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*?])[a-zA-Z0-9!@#$%^&*?]{8,}$", message="영문, 숫자, 특수문자 중 2종류 이상을 조합하여 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 입력해 주세요."), EqualTo('password2', '비밀번호가 일치하지 않습니다'), Length(min=8, message='')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호를 한번 더 입력해주세요.')])
    email = EmailField('이메일', [DataRequired('이메일은 필수 입력 항목입니다.'), Email('이메일 형식으로 입력해주세요.')])

class UserLoginForm(FlaskForm):
    email = EmailField('이메일', [DataRequired('이메일을 입력해주세요.'), Email('이메일 형식으로 입력해주세요')])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력해주세요')])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요')])