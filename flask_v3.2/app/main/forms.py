from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('请填写姓名', validators=[DataRequired()])
    submit = SubmitField('确定')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('关于')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('关于')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用.')


class PostForm(FlaskForm):
    body = PageDownField("发布新公告", validators=[DataRequired()])
    submit = SubmitField('发布')

class AddManage(FlaskForm):
    usename = StringField("连接数据库账户", validators=[DataRequired()])
    passwd = StringField("连接数据库密码", validators=[DataRequired()])
    ip = StringField("连接数据库IP", validators=[DataRequired()])
    dbname = StringField("连接数据库名称", validators=[DataRequired()])
    ser_name = StringField("TNS名称", validators=[DataRequired()])
    type = StringField("连接数据库类型", validators=[DataRequired()])
    sysname = StringField("新建系统名称", validators=[DataRequired()])
    sys_id = StringField("新建数据库名称", validators=[DataRequired()])
    submit = SubmitField('添加')




