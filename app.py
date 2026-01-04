import os
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from database import db
from models import User


#Flask application reset
app = Flask(__name__)

#Database setting
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #불필요한 이벤트 처리 비활성화 

#creating DB
db.init_app(app)

#default path
@app.route('/')
def home() :
    return {"message" : "서버가 정상적으로 실행중입니다.", "status": "success"}

@app.route('/register', methods=['POST'])
def register() :
    #data from client
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error" : "아이디와 비밀번호를 확인이 필수입니다"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error" : "이미 사용 중인 아이디입니다."}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "회원가입 성공!", "username": username}), 201

# app execution (debug = True, 코드가 수정될 때마다 서버가 자동 재시작.)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("데이터베이스 테이블이 생성되었습니다!") # 확인 메시지

    app.run(debug=True)

