from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Hostels, User
from market.forms import RegisterForm, LoginForm, RegisterHostel
from market import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    hostels = Hostels.query.all()
    return render_template('search.html', hostels=hostels)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('search_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('search_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/registerhostel', methods=['GET', 'POST'])
def add_hostel():
    form = RegisterHostel()
    if form.validate_on_submit():
        hs_name = request.form['hs_name']
        hs_address = request.form['hs_address']
        hs_contact = request.form['hs_contact']
        hs_rent = request.form['hs_rent']
        hs_description = request.form['hs_description']
        rooms = request.form['rooms']
        caution = request.form['caution']
        curfew = request.form['curfew']
        maps_link = request.form['maps_link']
        type = request.form['type']
        record = Hostels(hs_name=form.hs_name.data, hs_address=form.hs_address.data, hs_contact=form.hs_contact.data, hs_rent=form.hs_rent.data, hs_description=form.hs_description.data, rooms=form.rooms.data, caution=form.caution.data, curfew=form.curfew.data, maps_link=form.maps_link.data, type=form.type.data)
        db.session.add(record)
        db.session.commit()
        return render_template('search.html')
    else:
        return render_template('registerhostel.html', form=form)

@app.route('/search_page', methods=['GET', 'POST'])
def searches():
    q=request.args.get('q')
    
    if db.session.query(db.exists().where(Hostels.hs_name == q)).scalar():
        form=Hostels.query.filter(Hostels.hs_name.contains(q))
        return render_template('search_results.html', hostels=form)
    else:
        flash('We couldn\'t find any match to your query', category='danger')
        return render_template('search_results.html')
    
