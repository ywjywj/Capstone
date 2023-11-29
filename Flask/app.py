import qrcode
from random import *
from pymongo import MongoClient
from flask import Flask, request,send_file,render_template
from waitress import serve
client = MongoClient('mongodb+srv://pub:mYHzd2SF5u1YWZvf@cluster0.uvvou5w.mongodb.net/?retryWrites=true&w=majority')
db = client.mydb
app = Flask(__name__)
@app.route("/")
def hello_word():
    return render_template('index.html')

@app.route("/QR")
def index():
    # 사용자에게 URL을 입력하라는 메시지를 표시합니다.
    pwd = request.args.get("p")
    doc = {'player':pwd}
    db.users.insert_one(doc)
    # QR 코드를 생성합니다.
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L
    )
    qr.add_data(pwd)
    qr.make()
    # QR 코드를 이미지로 저장합니다.
    img = qr.make_image(fill_color="black", back_color="white")
    i = str(random())
    img.save("static/qrcode"+i+".png")

    # QR 코드를 응답으로 반환합니다.
    return send_file("static/qrcode"+i+".png", mimetype="image/png")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)