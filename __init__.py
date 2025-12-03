from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #co


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/contact/')
def contact():
    return render_template('contact.html') #co

@app.route("/histogramme/")
def histogramme():
    temperatures = [
        ["Jour", "Température"],
        ["Lundi", 12],
        ["Mardi", 15],
        ["Mercredi", 14],
        ["Jeudi", 18],
        ["Vendredi", 17],
        ["Samedi", 20],
        ["Dimanche", 19]
    ]

    return render_template("histogramme.html", data=temperatures)



app = Flask(__name__)


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # Appel API GitHub avec User-Agent obligatoire
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        return f"Erreur API GitHub : {response.status_code}", 500

    commits = response.json()
    minutes_count = {}

    for c in commits:
        try:
            if "commit" not in c or "author" not in c["commit"]:
                continue

            date_string = c["commit"]["author"]["date"]

            # Supprimer millisecondes si elles existent
            date_string = date_string.split(".")[0] + "Z"

            date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            minute = date_obj.minute

            minutes_count[minute] = minutes_count.get(minute, 0) + 1

        except Exception as e:
            print("Erreur commit :", e)
            continue

    labels = list(minutes_count.keys())
    values = list(minutes_count.values())

    return render_template("commits.html", labels=labels, values=values)

  
if __name__ == "__main__":
  app.run(debug=True)
