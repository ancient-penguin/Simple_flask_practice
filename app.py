import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Memo


#Flask application reset
app = Flask(__name__)

#Database setting
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #불필요한 이벤트 처리 비활성화 

#한글 에러 처리
app.json.ensure_ascii = False

#JWT secret key
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

#creating DB
db.init_app(app)

#JWT manger reset
jwt = JWTManager(app)

#default path
@app.route('/')
def home() :
    return {"message" : "서버가 정상적으로 실행중입니다.", "status": "success"}

#회원가입 api
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

#로그인 api
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)

        return jsonify({
            "message" : "로그인 성공",
            "access_token": access_token
        }), 200
    else :
        return jsonify({"message" : "로그인 실패"}), 401

#writing memo
@app.route('/memo', methods=['POST'])
@jwt_required()
def create_memo() :
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()

    data = request.get_json()
    content = data.get('content')

    if not content :
        return jsonify({"message" : "내용이 없습니다."}), 400
    
    new_memo = Memo(content = content, user_id=user.id)
    db.session.add(new_memo)
    db.session.commit()

    return jsonify({"message" : "메모가 저장되었습니다."}), 201

#viewing memo
@app.route('/memo', methods=['GET'])
@jwt_required()
def get_memos():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()

    memos = user.memos

    output = []
    for memo in memos :
        output.append({"id" : memo.id, "content" : memo.content})

    return jsonify({"memos" : output}), 200

#update memo
@app.route('/memo/<int:memo_id>', methods=['PUT'])
@jwt_required()
def update_memos(memo_id):
    current_username = get_jwt_identity()

    memo = Memo.query.get_or_404(memo_id)

    if memo.author.username != current_username :
        return jsonify({"message" : "수정 권한이 없습니다. "}), 403

    data = request.get_json()
    new_content = data.get('content')

    if new_content :
        memo.content = new_content
        db.session.commit()
        return jsonify({"message" : "메모가 수정되었습니다.", "content": memo.content}), 200
    else :
        return jsonify({"message" : "내용을 입력해주세요."}), 400
    
#delete memo
@app.route('/memo/<int:memo_id>', methods=['DELETE'])
@jwt_required()
def delete_memo(memo_id) :
    current_username = get_jwt_identity()

    memo = Memo.query.get_or_404(memo_id)

    if memo.author.username != current_username:
        return jsonify({"message" : "삭제 권한이 없습니다."}), 403
    
    db.session.delete(memo)
    db.session.commit()

    return jsonify({"message" : "메모가 삭제되었습니다."}), 200


# app execution (debug = True, 코드가 수정될 때마다 서버가 자동 재시작.)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("데이터베이스 테이블이 생성되었습니다!") # 확인 메시지

    app.run(debug=True, host='0.0.0.0', port=5000) 