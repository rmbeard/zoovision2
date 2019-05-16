# Created by Rachel Beard: last updated 1/11/19
# Purpose: This is the entry point for a flask application that serves to
# Zoovision, a spatial decision support web application
import logging
from flask import render_template,  request
# from flask_bootstrap import Bootstrap
# from flask_nav import Nav
# from flask_nav.elements import Navbar, Subgroup, View, Link, Text
# from flask_googlemaps import GoogleMaps
# from wtforms import SelectField, SubmitField, Form, TextField, TextAreaField, validators
# from flask_wtf import FlaskForm
from map import maps1, maps2, sum_chart, local_moran_test
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session
# from db_setup import init_db

app = Flask(__name__)
# Bootstrap(app)
# nav = Nav(app)

# nav.register_element('my_navbar', Navbar('thenav', View('Home', 'home')))

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Circe2635!@localhost/zoovision'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation
# app.secret_key = 'secret key'
#
# # Set up database
# engine = create_engine('postgresql://postgres:Circe2635!@localhost/zoovision', convert_unicode=True)
# db = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# db = SQLAlchemy(app)

# init_db()


@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.route("/", methods=['GET', 'POST'])
def home():
    file = "./data/Export_Output.shp"
    # file = "C:\zoovision\data\Export_Output.shp"
    # set default parameters
    seasons = ['2015-16', '2016-17', '2017-18', '2018-19']
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas']
    weights = ['Distance', 'Genetic transition rate']
    risk_factors = ["ILI POSITIVE", 'PERCENT POSITIVE', '%UNWEIGHTED ILI']
    week = ''
    if request.method == 'GET':
        session['selected_risk'] = "ILI POSITIVE"
        session['selected_season'] = '2015-16'
        session['selected_week'] = 0
        session['selected_state'] = 'Alabama'
        session['selected_weight'] = 'Distance'
        selected_risk = session['selected_risk']
        selected_season = session['selected_season']
        selected_week = session['selected_week']
        selected_state = session['selected_state']
        selected_weight = session['selected_weight']
    elif request.method == 'POST':
        if 'Query' in request.form:
            selected_season = request.form['season']
            # selected_weight = request.form['weight']
            selected_risk = request.form['risk_factor']
            session['selected_risk'] = selected_risk
            session['selected_season'] = selected_season
            # session['selected_weight'] = selected_weight
            selected_week = session['selected_week']
            selected_state = session['selected_state']
            selected_weight = session['selected_weight']
            print(selected_risk)
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, week=week, min=40, max=52, selected_week=selected_week, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, risk_factors=risk_factors, result=result, chart=chart)
        elif 'hello' in request.form:
            selected_week = request.form['week']
            selected_week = int(selected_week)
            print(type(selected_week))
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            selected_risk = session['selected_risk']
            selected_weight = session['selected_weight']
            selected_season = session['selected_season']
            selected_state = session['selected_state']
            session['selected_week'] = selected_week
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, risk_factors=risk_factors,
                                   result=result, chart=chart)
        elif 'state' in request.form:
            selected_state = request.form['state']
            selected_state = int(selected_state)
            print(type(selected_state))
            selected_week = session['selected_week']
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            selected_risk = session['selected_risk']
            selected_weight = request.form['weight']
            selected_season = session['selected_season']
            session['selected_state'] = selected_state
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, risk_factors=risk_factors,
                                   result=result, chart=chart)
        elif 'case' in request.form:
            selected_risk = request.form['risk_factor']
            session['selected_risk'] = selected_risk
            selected_weight = request.form['weight']
            selected_week = session['selected_week']
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            selected_state = session['selected_state']
            selected_week = session['selected_week']
            selected_season = session['selected_season']
            print(selected_week)
            result_cluster = local_moran_test(file, selected_risk, selected_season, selected_val, selected_weight, selected_week)
            chart = sum_chart()
            result = maps2(file, selected_risk, selected_season, selected_val)
            return render_template("tab.html", weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, risk_factors=risk_factors,
                                   result=result, chart=chart, result_cluster=result_cluster)
    # chart = sum_chart(selected_risk, selected_season)
    if selected_week < 13:
        selected_val = selected_week + 40
    else:
        selected_val = selected_week - 12
    result = maps1(file, selected_risk, selected_season, selected_val)
    # result = "C:\zoovision\static\default.png"
    chart = sum_chart()
    return render_template("tab.html", weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, week=week, min=40, max=52, seasons=seasons, selected_week=selected_week,
                           selected_risk=selected_risk, selected_season=selected_season,
                           risk_factors=risk_factors,
                           result=result, chart=chart)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
