# _*_ coding:utf-8 _*_
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from app.admin.forms import LoginForm,PwdForm,CategoryForm,FoodForm,TravelsForm
from app.models import Admin,Category,User,Food,Record
from sqlalchemy import or_
from functools import wraps


@admin.route("/food/add/", methods=["GET", "POST"])
@admin_login
def food_add():
    """
    添加菜品页面
    """
    form = FoodForm() # 实例化form表单
    form.cate_id.choices = [(v.id, v.name) for v in Category.query.all()] # 为cate_id添加属性
    if form.validate_on_submit():
        data = form.data
        # 判断菜品是否存在
        food_count = Food.query.filter_by(name=data["name"]).count()
        # 判断是否有重复数据。
        if food_count == 1 :
            flash("菜品已经存在！", "err")
            return redirect(url_for('admin.food_add'))

        # 为Scenic类属性赋值
        food = Food(
            name=data["name"],
            cate_id = data["cate_id"],
        )
        db.session.add(food)  # 添加数据
        db.session.commit()     # 提交数据
        flash("添加美食成功！", "ok") # 使用flash保存添加成功信息
        return redirect(url_for('admin.food_add')) # 页面跳转
    return render_template("admin/food_add.html", form=form) # 渲染模板

@admin.route("/food/list/", methods=["GET"])
@admin_login
def food_list():
    """
    菜品列表页面
    """
    name = request.args.get('name','',type=str)   # 获取查询标题
    page = request.args.get('page', 1, type=int)   # 获取page参数值
    if name :                                     # 根据名称搜索菜品
        page_data = Food.query.filter(Food.name.like("%" + name + "%")).order_by(
            Food.addtime.desc()                    # 根据添加时间降序
        ).paginate(page=page, per_page=5)          # 分页
    else :                                         # 显示全部菜品
        page_data = Food.query.order_by(
            Food.addtime.desc()                  # 根据添加时间降序
        ).paginate(page=page, per_page=5)          # 分页
    return render_template("admin/food_list.html", page_data=page_data) # 渲染模板

@admin.route("/food/edit/<int:id>/", methods=["GET", "POST"])
@admin_login
def food_edit(id=None):
    """
    编辑菜品页面
    """
    form = FoodForm() # 实例化ScenicForm类
    form.cate_id.choices = [(v.id, v.name) for v in Category.query.all()]  # 为cate_id添加属性
    food = Food.query.get_or_404(int(id)) # 根据ID查找菜品是否存在
    if request.method == "GET":        # 如果以GET方式提交，获取所有菜品信息
        form.cate_id.data = food.cate_id
    if form.validate_on_submit():     # 如果提交表单
        data = form.data              # 获取表单数据
        food_count = Food.query.filter_by(name=data["name"]).count()  # 判断标题是否重复
        # 判断是否有重复数据
        if food_count == 1 and food.name != data["name"]:
            flash("菜品已经存在！", "err")
            return redirect(url_for('admin.food_edit', id=id))

        # 属性赋值
        food.name = data["name"]
        food.cate_id = data["cate_id"]
        db.session.add(food)   # 添加数据
        db.session.commit()    # 提交数据
        flash("修改菜品成功！", "ok")
        return redirect(url_for('admin.food_edit', id=id)) # 跳转到编辑页面
    return render_template("admin/food_edit.html", form=form, food=food) # 渲染模板，传递变量


@admin.route("/food/", methods=["GET"])
@admin_login
def food_del():
    """
    菜品删除
    """
    id = request.args.get('id')
    res = {}
    try:
        food = Food.query.filter_by(id=id).first_or_404()
        res['status']  = 1
        res['message'] =  "菜品<<{0}>>删除成功".format(food.name)
        db.session.delete(food)
        db.session.commit()
    except:
        res['status']  = -1
        res['message'] =  "菜品<<{0}>>删除失败".format(food.name)
    return jsonify(res)