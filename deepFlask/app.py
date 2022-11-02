from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainpage.html')
    
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()#json 데이터를 받아옴
    return jsonify(user)# 받아온 데이터를 다시 전송
 
@app.route('/environments/<language>')
def environments(language):
    return jsonify({"language":language})
 
 