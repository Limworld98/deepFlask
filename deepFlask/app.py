from flask import Flask, json, jsonify, render_template, request

from EffiModule import (
    extract500,
    extract_result,
    validate,
    get_ocr_result,
    final_candidates,
)

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
        print("======================PILL IDENTIFICATION START===================")
        identifier = request.form["identifier"]
        # path should be modified
        # path should be removed when it combined with front-backend
        img_path = "../data/good_image/reference_image_500/199600094/199600094.jpg"
        identifier_list = extract500(identifier)

        pred_class = validate(
            identifier_list,
            "model_best.pth",
            img_path,
        )

        result = final_candidates(pred_class, identifier, img_path)

        print("======최종 검출 목록====== ")
        print(result)
    return render_template("output.html", result=result)


#사진 전송받는 모듈, POST형태로 사진 날리면 good_image/userimage안에 image로 저장됨
@app.route("/imageload", methods=["GET", "POST"]) 
def imageload():

    f = request.files["img"]
    f.save("../data/good_image/userimage/" + "image.jpg")
    return "send complete"

#json 데이터 전송받고 딥러닝 돌리는 모듈, POST형태로 json 데이터 받으면, 파싱해서 identifier 추출하고 json형태로 결과 반환
@app.route("/deepjson", methods=["GET", "POST"])
def result():

    received = request.get_json()
    print(received["identifier"])

    identifier = received["identifier"]
    # # path should be modified
    # # path should be removed when it combined with front-backend
    img_path = "../data/good_image/userimage/image.jpg"

    identifier_list = extract500(identifier)

    pred_class = validate(
        identifier_list,
        "model_best.pth",
        img_path,
    )

    result = final_candidates(pred_class, identifier, img_path)

    print("======최종 검출 목록====== ")
    print(result)

    jsonResult = json.dumps(result, ensure_ascii=False)
    print(jsonResult)
    return jsonResult
