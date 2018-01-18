# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import session
from flask.ext.login import current_user

from flask_login import login_required, login_user, logout_user

from dataDisplay.extensions import login_manager
from dataDisplay.flaskapp.myfunc import cal_permission, int2bin
from dataDisplay.public.forms import LoginForm
from dataDisplay.user.forms import RegisterForm
from dataDisplay.user.models import User, Role
from dataDisplay.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """login page."""
    form = LoginForm(request.form)
    # Handle logging in
    if 'user_id' not in session:
        if request.method == 'POST':
            if form.validate_on_submit():
                login_user(form.user)
                session['permission'] = int2bin(current_user.department)
                # flash('You are logged in.', 'success')
                redirect_url = request.args.get('next') or url_for('data.dashboard')
                return redirect(redirect_url)
            else:
                flash_errors(form)
        return render_template('public/login.html', form=form)
    return redirect(url_for('data.dashboard'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('您已注销成功', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        department, permission, town = cal_permission(form)
        User.create(username=form.username.data, password=form.password.data, department=department,
                    name=form.role_name.data, town=town, active=1)
        # 分配权限x
        user = User.query.filter(User.username == form.username.data)[0]
        role = Role(permissions=permission)
        user.roles.append(role)
        user.update()

        # flash('Thank you for registering. You can now log in.', 'success')
        return redirect('/tables/User')
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
