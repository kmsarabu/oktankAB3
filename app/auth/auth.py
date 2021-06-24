from flask import Blueprint, Flask , jsonify, render_template, session, request, redirect, url_for
from flask_login import login_user, logout_user
from app.models import User, Kart
from .forms import RegistrationForm, LoginForm

auth_bp = Blueprint("auth_bp", __name__, template_folder="templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def main():
	if request.method == "POST":
		form = LoginForm()
		user= User()
		email = request.form['email']
		password = request.form['password']
		result = user.verify(email, password)
		if result == True:
			login_user(email) 
			flask.flash('Logged in successfully')
			session['email'] = email
			products = Kart().view(email)
			productList = []
			for x in products:
				r = x.get('qty')
				if r is None:
					r = 1
				for z in range(r):
					productList.append(x['productid'])
			session['Kart'] = productList
			return redirect(url_for("general_bp.home"))
	return render_template("login.html", title="Login")

@auth_bp.route("/register", methods=["GET","POST"])
def signup():
	if request.method == "POST":
		form = LoginForm()
		user= User()
		fname = request.form['fname']
		lname = request.form['lname']
		email = request.form['email']
		password = request.form['password']
		user.add(fname,lname, email, password)
		return redirect(url_for("auth_bp.main"))
	else:
		return render_template("signup.html", title ="register")

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_pass():
	return render_template("forgot_password.html", title="forgot password")

@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('Kart', None)
    session.clear()
    logout_user()
    #return redirect("/")
    return redirect(url_for("general_bp.home"))

@auth_bp.route("/account")
def account():
    if session.get('email'):
        user = User()
        result = [dict(p) for p in user.get(session['email'])]
        return render_template("account.html", title="Account", acctinfo=result)
    else:
        return redirect(url_for("general_bp.home"))
