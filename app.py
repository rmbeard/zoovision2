# Created by Rachel Beard: last updated 4/11/19
# Purpose: This is the entry point for a flask application that serves to
# Zoovision, a spatial decision support web application
import logging
from flask import render_template,  request
from map import maps1, sum_chart
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
    file = "./data/Export_Output.shp"
    seasons = ['2016-17', '2017-18', '2018-19']
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas']
    viruses = ['H1N1', 'H3N2']
    risk_factors = ['PERCENT POSITIVE', '%UNWEIGHTED ILI']
    week = ''
    if request.method == 'GET':
        session['selected_risk'] = "PERCENT POSITIVE"
        session['selected_season'] = '2015-16'
        session['selected_week'] = 0
        session['selected_state'] = 'Alabama'
        selected_risk = session['selected_risk']
        selected_season = session['selected_season']
        selected_week = session['selected_week']
        selected_state = session['selected_state']
    elif request.method == 'POST':
        if 'Query' in request.form:
            selected_season = request.form['season']
            # selected_virus = request.form['virus']
            selected_risk = request.form['risk_factor']
            session['selected_risk'] = selected_risk
            session['selected_season'] = selected_season
            selected_week = session['selected_week']
            selected_state = session['selected_state']
            print(selected_week)
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", states=states, selected_state=selected_state, week=week, min=40, max=52, selected_week=selected_week, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season,
                                   viruses=viruses, risk_factors=risk_factors, result=result, chart=chart)
        elif 'hello' in request.form:
            selected_week = request.form['week']
            selected_week = int(selected_week)
            print(type(selected_week))
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week - 12
            selected_risk = session['selected_risk']
            selected_season = session['selected_season']
            selected_state = session['selected_state']
            session['selected_week'] = selected_week
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, viruses=viruses, risk_factors=risk_factors,
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
            selected_season = session['selected_season']
            session['selected_state'] = selected_state
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", states=states, selected_state=selected_state, selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, viruses=viruses, risk_factors=risk_factors,
                                   result=result, chart=chart)
    # chart = sum_chart(selected_risk, selected_season)
    if selected_week < 13:
        selected_val = selected_week + 40
    else:
        selected_val = selected_week - 12
    result = maps1(file, selected_risk, selected_season, selected_val)
    # result = "C:\zoovision\static\default.png"
    chart = sum_chart()
    return render_template("tab.html", states=states, selected_state=selected_state, week=week, min=40, max=52, seasons=seasons, selected_week=selected_week,
                           selected_risk=selected_risk, selected_season=selected_season, viruses=viruses,
                           risk_factors=risk_factors,
                           result=result, chart=chart)




if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)

