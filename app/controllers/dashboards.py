#importando o app do projeto principal
from app import app
from flask import render_template

@app.route('/dashboards')
def dashboards():
    return render_template('dashboards.html')