from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app,jsonify
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,AddManage
from .. import db
from ..models import Permission, Role, User, Post
from ..database_model import *
from ..decorators import admin_required
import datetime,time,random
from .manager_object import runconn





@main.route('/', methods=['GET'])
def index():
    test = request.args.get('test',type=str)

    #示例
    # point_data = {'title': '健康指数', 'num': '100', 'unit': '分', 'trend': 'down', 'underName':'基准分数','underValue': '80', 'imgType': '1', 'colorType': '2'}
    point_data2 = {'title': '告警(ora11g1)', 'num': '10', 'unit': '条', 'trend': 'down','underName':'总告警数','underValue': '10', 'imgType': '1', 'colorType': '2'}
    #point_chart = [{'name':'AAA','data':[15,12,10]},{'name':'BBB','data':[15,12,10]}]

    #获取point_data的相关信息
    p_ob_sid = aop_object_score.query.order_by(aop_object_score.score).first().sys_id
    p_ob_obid = aop_object_score.query.order_by(aop_object_score.score).first().object_id
    p_ob_name = aop_object_score.query.order_by(aop_object_score.score).first().instance_name
    p_ob_score = str(float(aop_object_score.query.order_by(aop_object_score.score).first().score))
    p_ob_bl_score = '80'
    point_data = {'title': '健康指数'+ '(' + p_ob_name + ')', 'num': p_ob_score, 'unit': '分', 'trend': 'down', 'underName':'基准分数','underValue': p_ob_bl_score, 'imgType': '1', 'colorType': '1'}

    #获取当前时间
    current_time = time.strftime('%H',time.localtime())

    point_chart = []
    #查找指定数据库的分值内容
    p_md_list = aop_model_score.query.filter(aop_model_score.sys_id==p_ob_sid,
                                             aop_model_score.object_id==p_ob_obid,
                                             aop_model_score.model_id%100==0).all()

    #告警值比例设定
    war_percent = 0.8
    #合成柱状图数据
    for p_md in p_md_list:
        #注意此处的hzmc_month。在之后的迭代时注意将此参数转化为形参。根据上文中的sys_id来找不同的数据库获取
        p_md_baseline = hzmc_month.query.filter(hzmc_month.hour==current_time,
                                                hzmc_month.score_name==p_md.table_name,
                                                hzmc_month.inst_id==1)\
                        .order_by(hzmc_month.time.desc()).first().base_line

        point_chart.append({'name': p_md.model_name,
                            'data': [random.randint(50, 100), round(p_md_baseline * war_percent),
                                                              round(p_md_baseline * (1 - war_percent))]})
        #随机生成/模拟数据用 float(p_md.score)


    system_list, object_list, model_list = left_nav()
    return render_template('index.html',point_data=point_data,point_data2=point_data2,point_chart=point_chart,system_list=system_list,object_list=object_list,model_list=model_list)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

#目标管理-第一页
@main.route('/management',methods=['GET','POST'])
@login_required
def management():
    #mainpoint in page
    page = request.args.get('page', 1, type=int)
    pagination = aop_system.query.order_by(aop_system.score).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    #left navigation list
    system_list,object_list,model_list=left_nav()
    return render_template('management.html',posts=posts,
                           system_list=system_list,object_list=object_list,model_list=model_list,
                           pagination=pagination)

#目标管理-第二页
@main.route('/management/<sys_id>',methods=['GET','POST'])
@login_required
def management_2(sys_id):
    sysname = request.args.get('sysname',type=str)
    #sysname是为了传递第一层名称,不能写在def的括号中。因为是请求
    page = request.args.get('page', 1, type=int)
    pagination = aop_object_score.query.filter_by(sys_id=sys_id).order_by(aop_object_score.score).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    system_list, object_list, model_list = left_nav()
    return render_template('management_2.html', posts=posts,sys_id=sys_id,
                           system_list=system_list, object_list=object_list, model_list=model_list,
                           sysname=sysname,pagination=pagination)

#目标管理-第三页
@main.route('/management/<sys_id>/<object_id>',methods=['GET','POST'])
@login_required
def management_3(sys_id,object_id):
    sysname = request.args.get('sysname')
    instance_name = request.args.get('instance_name')
    #instance是因为需要满足传递第二层名称
    page = request.args.get('page', 1, type=int)
    pagination = aop_model_score.query.filter_by(object_id=object_id).order_by(aop_model_score.score).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    system_list, object_list, model_list = left_nav()
    return render_template('management_3.html', posts=posts, sys_id=sys_id, object_id=object_id,
                           system_list=system_list, object_list=object_list, model_list=model_list,
                           sysname=sysname,instance_name=instance_name,pagination=pagination)

#@main.route('/目标管理')

#目标管理-性能图表
@main.route('/model/<table_name>',methods=['GET','POST'])
@login_required
def charts(table_name):
    # 本方法调用paint_table.进行数值查询。取出目标表字段end_time以及score
    sys_id = request.args.get('sys_id')
    object_id = request.args.get('object_id')
    sysname = request.args.get('sysname')
    instance_name = request.args.get('instance_name')
    stop_paint = False
    #表格名称
    if str.isdigit(table_name):
        chart_name = aop_model_score.query.filter_by(model_id=table_name).first().model_name + '详情'
    else:
        chart_name = aop_model_score.query.filter_by(table_name=table_name).first().model_name
    #异常判断
    if str.isdigit(table_name):
        table_name = int(table_name)
        try:
            chart_list = aop_model_score.query.filter(aop_model_score.model_id > table_name,
                                                      aop_model_score.model_id < (table_name + 100),
                                                      aop_model_score.sys_id == sys_id,
                                                      aop_model_score.object_id == object_id).all()
        except Exception as e:
            stop_paint = True
            print(Exception,"查询错误。请检查aop_model_score表")
            flash("查询错误。表不存在或异常")
            return redirect(url_for('.NoneValue',value="查询错误。请检查aop_model_score表"))
        list_table = []
        #初始化存放表单名称的列表
        dic_table = {}
        #初始化数据字典
        for i in chart_list:
            list_table.append(i.table_name)
            dic_table[i.table_name] = paint_table(i.table_name,sys_id,object_id)
    else:
        list_table = [table_name]
        # 初始化存放表单名称的列表;此处仅存放一个数值。为了保持list_table的类型一致。采用列表形式
        dic_table = {}
        # 初始化数据字典
        dic_table[table_name] = paint_table(table_name,sys_id,object_id)


    #语法校验,检查表格长度
    for list_tests in list_table:
        try:
            test_num1 = dic_table[list_tests]['end_time']
            test_num2 = dic_table[list_tests]['score1']
            if len(test_num1)<1 or len(test_num2)<1:
                stop_paint = True
        except Exception as e:
            print(Exception,"查询错误。表为空")
            stop_paint = True
            return redirect(url_for('.NoneValue', value="查询错误。请检查表内容是否为空"))

    if stop_paint is True:
        flash("查询错误。停止生成表。请检查数据库中是否存在该表或表中是否有数据")
        return redirect(url_for('.NoneValue',value="查询错误。停止生成表。请检查数据库中是否存在该表或表中是否有数据"))

    system_list, object_list, model_list = left_nav()
    return render_template('charts.html',sys_id=sys_id,object_id=object_id,table_name=table_name,
                           sysname=sysname,instance_name=instance_name,chart_name=chart_name,
                               system_list=system_list, object_list=object_list, model_list=model_list,
                           dic_table=dic_table,list_table=list_table)

@login_required
def paint_table(table_name,sys_id,object_id):
    adict = globals()
    end_time = []
    score1 = []
    #查询表的中文名
    table_cn_name = aop_model_score.query.filter_by(table_name=table_name,sys_id=sys_id,object_id=object_id).first().model_name
    #score2 = []
    try:
        #根据Inst_id进行分类。默认设定Inst_id仅有一种情况
        post1 = adict['%s' % table_name].query.filter_by(inst_id=1).all()
        #post2 = adict['%s' % table_name].query.filter_by(inst_id=2).all()
    except Exception as e:
        print(Exception, "查询错误。表不存在或异常")
        flash("查询错误。表不存在或异常")
        return redirect(url_for('.NoneValue',value="查询错误。表不存在或异常"))
    for i in post1:
        end_time.append(datetime.datetime.strftime(i.end_time, '%y-%m-%d %H:%M:%S'))
        score1.append(i.score)
    # for j in post2:
    #     score2.append(j.score)
    dict_values = {'end_time':end_time,'score1':score1,'table_cn_name':table_cn_name}
    return dict_values


@main.route('/<value>',methods=['GET','POST'])
def NoneValue(value):
    return render_template('None.html',value=value)


def left_nav():
    system_list = aop_system.query.all()
    object_list = aop_object_score.query.all()
    model_list = aop_model_score.query.all()
    return system_list,object_list,model_list

@main.route('/添加目标',methods=['GET','POST'])
@login_required
def add_manage():
    form = AddManage()
    request_code = runconn(
        user = form.usename.data,
        passwd = form.passwd.data,
        ip = form.ip.data,
        name = form.dbname.data,
        ser_name = form.ser_name.data,
        type = form.type.data,
        sysname = form.sysname.data,
        sys_id = form.sys_id.data
    )
    flash(request_code)
    system_list, object_list, model_list = left_nav()
    return render_template('add_manage.html',system_list=system_list, object_list=object_list, model_list=model_list,
                           form=form)





@main.route('/test',methods=['GET','POST'])
def test():
    return render_template('death.html')

#告警管理
@main.route('/report',methods=['GET','POST'])
def report():
    return render_template('report.html')