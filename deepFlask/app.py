from flask import Flask, render_template, jsonify, request
from EffiModule import extract500, validate

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("mainpage.html")


@app.route("/userinput")
def userinput():
    return render_template("userinput.html")


@app.route("/output", methods=["GET", "POST"])
def output():
    if request.method == "POST":
        identifier = request.form["identifier"]
        ident_list = extract500(identifier)
        # path should be modified
        pred_class = validate(
            ident_list,
            "model_best.pth",
            "../data/good_image/consumer_image/195900001/195900001.jpg",
        )
    return render_template("output.html", pred_class=pred_class)
