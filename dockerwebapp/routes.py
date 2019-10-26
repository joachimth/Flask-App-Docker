from flask import render_template, url_for, flash, redirect, request, abort, session
from dockerwebapp import app, db, bcrypt, login_manager
from dockerwebapp.forms import LoginForm,ChangePasswordForm
from dockerwebapp.models import User
from dockerwebapp.dockerinfo import dockerinfo
from flask_login import login_user, current_user, logout_user, login_required


#Docker Home Page
@app.route('/home')
@login_required
def home():
	version = dockerinfo.get('Version')
	return render_template('home.html',title='Home',version=version)

#Docker Web App Login Page
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check the username and password','danger')
	return render_template('login.html',title='Login',form=form)

#Change Password
@app.route('/change_password',methods=['GET','POST'])
@login_required
def changepassword():
	form = ChangePasswordForm()
	user = User.query.get(1)
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f"Your DockerAdmin password has been changed",'success')
	return render_template('change_password.html',form=form,title='Change Password')

#Logout
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))