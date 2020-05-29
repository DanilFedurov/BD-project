from flask import Flask, redirect, url_for, request, session, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, extract, func, update

from main import user_database, prediction_database, numerology_database
from forms.forms import User_registration, Add_prediction, Add_numerology_date, sign_in
from datetime import datetime
import random

import plotly
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask'
random.seed(20)

def connect():

    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{host}:{port}/{sid}'

    engine = create_engine( oracle_connection_string.format(

    username="SYSTEM",
    password="oracle",
    sid="XE",
    host="localhost",
    port="1521",
    database="PROJECT",
    ), echo=True)

    Session = sessionmaker(bind=engine)
    sessionn = Session()
    return sessionn


def pie(values1, values2):

    labels = ['Count of predictions in the database', 'Count of history events in the database'] 
    values = [values1, values2]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=['rgb(0,255,0)','rgb(0,206,209)'])])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def scatter(values1):

    months = ['Count of users']

    fig = go.Figure(data=go.Scatter(
    y=[values1],
    x=[1],
    mode='markers',
    marker=dict(size=[100],
                color=[2])
    ))

    fig.update_layout()

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route("/", methods = ['GET'])
def main():
    return render_template('Page1.html')


@app.route("/Page2", methods = ['GET'])
def page2():
    return render_template('Page2.html')


@app.route('/Page3', methods=["GET", "POST"])
def loginin():
    form = sign_in()
    if form.is_submitted():
        try:
            my_session = connect()
            result = request.form
            id_of_user = my_session.query(user_database.id_user).filter_by(user_login=result['user_login'], user_pass=result['user_pass']).all()
            print(id_of_user)
            if len(id_of_user):
                if result['user_login']=='admin'and result['user_pass']=='admin':
                    session['admin'] = 1
                else:
                    session['admin'] = 0
                return render_template('Page5.html',admin=session['admin'])
            else:
                return render_template('notOk.html', text = 'Invalid data', redir = 'login')
        except:
            return render_template('notOk.html', text = 'Invalid data', redir = 'login')
    return render_template('Page3.html', form = form)


@app.route('/Page4', methods=["GET", "POST"])
def registration():
    form = User_registration()
    if form.is_submitted():
        try:
            my_session = connect()
            result = request.form
            add = user_database(result['user_name'], result['user_surname'], result['user_age'], result['user_mail'], result['user_login'], result['user_pass'])
            my_session.add(add)
            my_session.commit()
            return render_template('Ok.html', text = 'Now u can sign in', redir='registration')
        except:
            result = request.form
            if len(result['user_age']) < 18:
                text = 'You are smaller then 18'
            else:
                text = 'This data has already used'
            return render_template('notOk.html', text=text, redir = 'registration')
        
    return render_template('Page4.html')

@app.route('/Page5')
def prediction_history():
    return render_template('Page5.html', admin=session['admin'])

@app.route('/Page6')
def showprediction():
    try:
        sessionn = connect()
        first_note = sessionn.query(prediction_database.id_pred).all()[0][0]
        number = random.randint(first_note, first_note -1+len(sessionn.query(prediction_database.id_pred).all()))
        text = sessionn.query(prediction_database.prediction_description).filter_by(id_pred=number).scalar()
    except:
        return render_template('notOk.html', text='Database is empty', redir = 'prediction')

    return render_template('Page6.html', text=text, admin=session['admin'])

@app.route('/Page7')
def numerologic():
    try:
        sessionn = connect()
        this_month = str(datetime.now().date().month)
        this_day = str(datetime.now().date().day)
        numer = sessionn.query(numerology_database.numerology_description).filter(extract('month', numerology_database.numerology_date) == this_month, extract('day', numerology_database.numerology_date) == this_day).all()
        if len(numer) == 0:
            return render_template('notOk.html', text='Database is empty', redir = 'numerologic')
    except:
        return render_template('notOk.html', text='Connection error', redir = 'numerologic')

    return render_template('Page7.html', numer=numer, admin=session['admin'])

@app.route('/adminpage', methods=['GET', 'POST'])
def adminfunc():

    form1 = Add_prediction()
    if form1.is_submitted() and form1.prediction_description.data:
        try:
            my_session = connect()
            result = request.form
            new_prediction = prediction_database(result['prediction_description'])
            my_session.add(new_prediction)
            my_session.commit()
            return render_template('Ok.html', text = 'You add new description', redir = 'admin')          
        except:
            return render_template('notOk.html', text = 'Your form is null', redir = 'admin')
    
    form2 = Add_numerology_date()
    if form2.is_submitted():
        try:
            my_session = connect()
            result = request.form
            print(result['numerology_date'])
            my_date = result['numerology_date'][8:10] +'.'+ result['numerology_date'][5:7] +'.'+ result['numerology_date'][0:4]
            new_numer_data = numerology_database(my_date, result['numerology_description'])
            my_session.add(new_numer_data)
            my_session.commit()
            return render_template('Ok.html', text = 'You add new history event', redir = 'admin')          
        except:
            return render_template('notOk.html', text = 'Your form is null', redir = 'admin')
           
    return render_template('admin.html')



@app.route('/graphs', methods=['GET', 'POST'])
def graph1():

    sessionn = connect()
    val1 = len(sessionn.query(prediction_database.id_pred).all())
    val2 = len(sessionn.query(numerology_database.id_nume).all())
    pie_graph = pie(val1, val2)

    if val1+val2 == 0:
    	check = 1
    else:
    	check = 0 
    val1 = len(sessionn.query(user_database.id_user).all())
    my_scatter = scatter(val1)

    return render_template('graphs.html', plot1=pie_graph, plot2=my_scatter, check = check)


if __name__ == "__main__":
    app.run(debug = True)