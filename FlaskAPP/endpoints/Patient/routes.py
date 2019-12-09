from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from FlaskAPP.endpoints.Login.forms import LoginForm
from FlaskAPP.models.testframe import TestFrame
patients = Blueprint('patients', __name__)


@login_required
@patients.route('/patients')
def index_view():
    if current_user.is_authenticated:
        return render_template('Patient/patients.html', user=current_user,
                               tableData=TestFrame.query.filter_by(DoctorID=current_user.DoctorID).all())
    else:
        return render_template('Login/login.html', form=LoginForm())

@patients.route('/patients/replay/')
def replay():
    if current_user.is_authenticated:
        return render_template('Patient/replay.html')
    else:
        return render_template('Login/login.html', form=LoginForm())