# Created by Rachel Beard: last updated 1/11/19
# Purpose: This is the entry point for a flask application that serves to
# Zoovision, a spatial decision support web application
import logging
from flask import Flask, Flask, render_template, flash, request, jsonify
# from flask_googlemaps import GoogleMaps
# from wtforms import SelectField, SubmitField, Form, TextField, TextAreaField, validators
# from flask_wtf import FlaskForm
from map import maps1, mapper, mapper_test, local_moran, slider
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
import os
from flask import Flask, session

# from db_setup import init_db

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Circe2635!@localhost/zoovision'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation
app.secret_key = 'secret key'

# Set up database
# engine = create_engine('postgresql://postgres:Circe2635!@localhost/zoovision', convert_unicode=True)
# db = scoped_session(sessionmaker(autocommit=False,
#                                 autoflush=False,
#                                bind=engine))
# db = SQLAlchemy(app)


# init_db()


@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.route("/", methods=['GET', 'POST'])
def home():
    # file = "C:\zoovision\data\states\states2.shp"
    # title = "United States"
    # result = mapper2(file, title)
    return render_template("home.html")


@app.route("/surveillance", methods=['GET', 'POST'])
def surveillance():
    # set filepeth to shapefile to use in geopandas
    # file = os.path.relpath('zoovision\data\state', 'states2.shp')
    file = "./data/state/states2.shp"
    # set defualt parametersx
    seasons = ['2015-16', '2016-17', '2017-18', '2018-19']
    viruses = ['H5N2', 'H5N8']
    risk_factors = ['PERCENT POSITIVE', '%UNWEIGHTED ILI']
    week = ''
    if request.method == 'GET':
        session['selected_risk'] = "PERCENT POSITIVE"
        session['selected_season'] = '2015-16'
        session['selected_week'] = 52
        selected_risk = session['selected_risk']
        selected_season = session['selected_season']
        selected_week = session['selected_week']
    elif request.method == 'POST':
        if 'Query' in request.form:
            selected_season = request.form['season']
            # selected_virus = request.form['virus']
            selected_risk = request.form['risk_factor']
            session['selected_risk'] = selected_risk
            session['selected_season'] = selected_season
            selected_week = session['selected_week']
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_week)

            return render_template("surveillance.html", week=week, min=1, max=52, selected_week=selected_week,
                                   seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season,
                                   viruses=viruses, risk_factors=risk_factors, result=result)
        elif 'hello' in request.form:
            selected_week = request.form['week']
            selected_week = int(selected_week)
            print(type(selected_week))
            selected_risk = session['selected_risk']
            selected_season = session['selected_season']
            session['selected_week'] = selected_week
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_week)
            return render_template("surveillance.html", selected_week=selected_week, week=week, min=1, max=52,
                                   seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, viruses=viruses,
                                   risk_factors=risk_factors,
                                   result=result)
    result = maps1(file, selected_risk, selected_season, selected_week)
    return render_template("surveillance.html", week=week, min=1, max=52, seasons=seasons, selected_week=selected_week,
                           selected_risk=selected_risk, selected_season=selected_season, viruses=viruses,
                           risk_factors=risk_factors,
                           result=result)


@app.route("/prediction_analysis", methods=['GET', 'POST'])
def prediction_analysis():
    # set defualt parameters
    file = "./data/region1/Region1.shp"
    weights = ['Genetic transition rate', 'Inverse Distance']
    selected_weight = "Inverse Distance"
    selected_risk = "POP2010"
    selected_species = "Public Health"
    speciess = ['Public Health', 'Wildlife', 'Agriculture']
    risk_factors = ['POP10_SQMI', 'POP2000', 'POP2010', 'Prevalence']
    if request.method == 'POST':
        selected_species = request.form['species']
        selected_weight = request.form['weight']
        # selected_risk = request.form['risk_factor']
        if selected_species == 'Public Health':
            # set filepeth to shapefile to use in geopandas
            file = "./data/region1/Region1.shp"
            # db_result = engine.execute('SELECT * FROM human_data WHERE season_description = 2017')
            # df = GeoDataFrame(db_result.fetchall())
            # df.columns = db_result.keys()
            # print(data(df))
        elif selected_species == 'Wildlife':
            db_result = engine.execute('SELECT * FROM avian_data')
        # result = mapper(file, db_result)
        # print(tuple(db_result))
        result = local_moran(file, selected_weight)
        return render_template("prediction_analysis.html", speciess=speciess, weights=weights,
                               selected_species=selected_species, selected_weight=selected_weight,
                               risk_factors=risk_factors, selected_risk=selected_risk, result=result)

    else:
        result = mapper(file)

    return render_template("prediction_analysis.html", speciess=speciess, selected_risk=selected_risk,
                           selected_species=selected_species, selected_weight=selected_weight, weights=weights,
                           risk_factors=risk_factors, result=result)


@app.route("/survey", methods=['GET', 'POST'])
def survey():
    selected_virus = "Genetic transition rate"
    selected_risk = "POP2010"
    selected_species = "Public Health"
    speciess = ['18-21', '22-26', '27-32', '33-37', '38-42', '43-47', '48+']
    viruses = ['High School', 'Undergraduate', 'Masters', 'Doctoral']
    risk_factors = ['None', '<1y', '2-4y', '5+']
    if request.method == 'POST':
        selected_species = request.form['species']
        selected_virus = request.form['virus']
        selected_risk = request.form['risk_factor']

    return render_template("survey.html", speciess=speciess, selected_risk=selected_risk,
                           selected_species=selected_species, selected_virus=selected_virus, viruses=viruses,
                           risk_factors=risk_factors)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# def slider():
#     df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
#
#     data = [dict(type='choropleth',
#                  locations=df['code'].astype(str),
#                  z=df['total exports'].astype(float),
#                  locationmode='USA-states')]
#
#     # let's create some additional, random data
#     for i in range(5):
#         data.append(data[0].copy())
#         data[-1]['z'] = data[0]['z'] * np.random.rand(*data[0]['z'].shape)
#
#     # let's create the steps for the slider
#     steps = []
#     for i in range(len(data)):
#         step = dict(method='restyle',
#                     args=['visible', [False] * len(data)],
#                     label='Year {}'.format(i + 1980))
#         step['args'][1][i] = True
#         steps.append(step)
#
#     sliders = [dict(active=0,
#                     pad={"t": 1},
#                     steps=steps)]
#     layout = dict(geo=dict(scope='usa',
#                            projection={'type': 'albers usa'}),
#                   sliders=sliders)
#
#     fig = dict(data=data,
#                layout=layout)
#     # py.plot(fig)
#
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return graphJSON


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
