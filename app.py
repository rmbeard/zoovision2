# Created by Rachel Beard: last updated 1/11/19
# Purpose: This is the entry point for a flask application that serves to
# Zoovision, a spatial decision support web application
from flask import render_template,  request
from map import maps1, maps2, sum_chart1, precalc_moran
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session

app = Flask(__name__)
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
    # file = "./data/Export_Output.shp"
    shapefile = "C:\zoovision\data\Export_Output.shp"
    # set default parameters
    seasons = ['2015-16', '2016-17', '2017-18', '2018-19']
    states = ['Alabama', 'Arizona', 'Arkansas','California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'MaryLand', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',  'West Virginia', 'Wisconsin', 'Wyoming']
    weights = ['Distance', 'Genetic transition rate']
    risk_factors = ["ILI POSITIVE", 'PERCENT POSITIVE', '%UNWEIGHTED ILI']
    strains = ["H1N1", 'H3N2']
    week = ''
    if request.method == 'GET':
        session['selected_risk'] = '%UNWEIGHTED ILI'
        session['selected_season'] = '2018-19'
        session['selected_week'] = 0
        session['selected_state'] = 'Alabama'
        session['selected_weight'] = 'Genetic transition rate'
        session['selected_strain'] = 'H3N2'
        selected_risk = session['selected_risk']
        selected_season = session['selected_season']
        selected_week = session['selected_week']
        selected_state = session['selected_state']
        selected_weight = session['selected_weight']
        selected_strain = session['selected_strain']
    elif request.method == 'POST':
        if 'Query' in request.form:
            selected_season = request.form['season']
            selected_risk = request.form['risk_factor']
            selected_strain = request.form['strain']
            session['selected_risk'] = selected_risk
            session['selected_season'] = selected_season
            session['selected_strain'] = selected_strain
            selected_week = session['selected_week']
            selected_state = session['selected_state']
            selected_weight = session['selected_weight']
            selected_strain = session['selected_strain']
            print(selected_strain)
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            result = maps1(shapefile, selected_risk, selected_strain, selected_season, selected_val)
            chart = sum_chart1(selected_val, selected_season, selected_state)
            return render_template("tab.html", strains=strains, weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, week=week, min=40, max=52, selected_week=selected_week, seasons=seasons,
                                   selected_risk=selected_risk, selected_strain=selected_strain, selected_season=selected_season, risk_factors=risk_factors, result=result, chart=chart)
        elif 'week' in request.form:
            selected_week = request.form['week']
            selected_week = int(selected_week)
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            selected_risk = session['selected_risk']
            selected_weight = session['selected_weight']
            selected_season = session['selected_season']
            selected_state = session['selected_state']
            selected_strain = session['selected_strain']
            session['selected_week'] = selected_week
            result = maps1(shapefile, selected_risk, selected_strain, selected_season, selected_val)
            chart = sum_chart1(selected_val, selected_season, selected_state)
            return render_template("tab.html", strains=strains, weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_strain=selected_strain, selected_season=selected_season, risk_factors=risk_factors,
                                   result=result, chart=chart)
        elif 'state' in request.form:
            selected_state = request.form['state']
            session['selected_state'] = selected_state
            selected_week = session['selected_week']

            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            print("entered state")
            selected_risk = session['selected_risk']
            selected_weight = session['selected_weight']
            selected_season = session['selected_season']
            selected_strain = session['selected_strain']
            # session['selected_state'] = selected_state

            result = maps1(shapefile, selected_risk, selected_strain, selected_season, selected_val)
            chart = sum_chart1(selected_val, selected_season, selected_state)
            return render_template("tab.html", strains=strains, weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_strain=selected_strain, selected_season=selected_season, risk_factors=risk_factors,
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
            selected_strain = session['selected_strain']
            # result_cluster = local_moran_test(file, selected_risk, selected_season, selected_val, selected_weight, selected_week)
            result_cluster = precalc_moran(shapefile, selected_season, selected_val, selected_weight)
            chart = sum_chart1(selected_val, selected_season, selected_state)
            result = maps2(shapefile, selected_strain, selected_risk, selected_season, selected_val)
            return render_template("tab.html", strains=strains, weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_strain=selected_strain, selected_season=selected_season, risk_factors=risk_factors,
                                   result=result, chart=chart, result_cluster=result_cluster)
    if selected_week < 13:
        selected_val = selected_week + 40
    else:
        selected_val = selected_week - 12
    result = maps1(shapefile, selected_risk, selected_strain, selected_season, selected_val)
    chart = sum_chart1(selected_val, selected_season, selected_state)
    return render_template("tab.html", strains=strains, weights=weights, selected_weight=selected_weight, states=states, selected_state=selected_state, week=week, min=40, max=52, seasons=seasons, selected_week=selected_week,
                           selected_risk=selected_risk, selected_strain=selected_strain, selected_season=selected_season,
                           risk_factors=risk_factors,
                           result=result, chart=chart)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
