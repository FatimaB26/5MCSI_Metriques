from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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


@app.route('/commits/')
def commits():
    # Récupération brute de tous les commits
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    # Dictionnaire minute → nombre de commits
    minutes_count = {}

    for commit in data:
        date_string = commit["commit"]["author"]["date"] 
        date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_obj.minute

        if minute not in minutes_count:
            minutes_count[minute] = 0
        minutes_count[minute] += 1

    # On transmet les minutes et les valeurs au template
    labels = list(minutes_count.keys())
    values = list(minutes_count.values())

    return render_template("commits.html", labels=labels, values=values)
  
if __name__ == "__main__":
  app.run(debug=True)
