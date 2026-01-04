import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Flask application reset
app = Flask(__name__)

#Database setting
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #불필요한 이벤트 처리 비활성화 

#creating DB
db = SQLAlchemy(app)

#default path
@app.route('/')
def home() :
    return {"message" : "서버가 정상적으로 실행중입니다.", "status": "success"}

# app execution
if __name__ == '__main__':
    app.run(debug=True)