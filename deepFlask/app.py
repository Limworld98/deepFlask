from flask import Flask, render_template, jsonify, request
from EffiModule import extract500 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainpage.html')
    
@app.route('/userinput')
def userinput():
    return render_template('userinput.html')

@app.route('/output', methods=['GET','POST'])
def output():
    if request.method == 'POST':
        identifier = request.form['identifier']
        extract500(identifier)
    return render_template('output.html')
 