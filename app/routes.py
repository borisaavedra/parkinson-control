from flask import render_template, url_for, redirect, flash, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, ParkinsonControl
from werkzeug.urls import url_parse
from datetime import datetime
from dateutil import tz
import sqlalchemy.exc


def get_control(base_query):
    '''Get the last 6 states from database'''
    control_dict = {}
    control_list = []
    n_register = 7
    n = 0
    base_query_len = base_query.count()

    get_state = lambda state: "On" if state == True else "Off"
    no_time = datetime(1,1,1)

    if base_query_len < n_register:
        n_register = base_query_len

    while n < n_register - 1:
        delta = no_time + (base_query[n].starttime - base_query[n + 1].starttime)
        control_dict["delta"] = delta.strftime("%H:%M:%S")
        # print("Hora de la base de datos {}".format(str(base_query[n + 1].starttime)))
        control_dict["date"] = base_query[n + 1].starttime.strftime("%d - %B - %Y | %I:%M %p")
        print("Hora DB despues de formateo {}".format(str(base_query[n + 1].starttime)))
        control_dict["status"] = get_state(base_query[n + 1].status)
        control_list.append(control_dict.copy())
        n += 1

    return control_list

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    user_id = current_user.id
    control_list = []
    first_entry = False
    control_db = ParkinsonControl.query.filter_by(user_id=user_id).order_by(ParkinsonControl.starttime.desc())
    if control_db.count() == 0:
        status_db = False
    else:
        status_db = control_db[0].status
    #####
        if control_db.count() > 1:
            control_list = get_control(control_db)
            print(f"Hora de la BASE DE DATOS: {control_list[0]['date']}")
        elif control_db.count() == 1:
            first_entry = True
    #####
    if request.method == "POST":
        status = bool(int(request.form["q"]))
        server_date = datetime.now()
        print(f" HORA DE SERVIDOR: {str(server_date)}")
        now_vzla = server_date.astimezone(tz.gettz("America/Caracas"))
        print(f" HORA DE VENEZUELA: {str(now_vzla)}")
        now = now_vzla
        control = ParkinsonControl(status=status, starttime=now_vzla, user_id=user_id)
        try:
            db.session.add(control)
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for("index"))
    return render_template("index.html", status_db=status_db, control_list=control_list, first_entry=first_entry)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))