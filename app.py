from flask import Flask, jsonify, request
from functools import wraps
import jwt

# TOKEN FOR POSTMAN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5MDAxLCJ1c2VybmFtZSI6IkRvc2szbiIsImxldmVsIjoibWFzdGVyIn0.-yfuRjLGUL_kKCa96UidXV_VErgmbDL79LZQk76cInY"

app = Flask(__name__)

app.config['SECRET_KEY']='shhh_this_is_a_secret!'

#MIDDLEWARE
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs) 
    return decorator

@app.route("/", methods=['GET'])
def main():
    return "<p>Welcome to the main page of the app!!</p>"

@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = [
        {'user_id': 9001, 'username': 'Dosk3n', 'level': 'master'},
        {'user_id': 9002, 'username': 'Jay', 'level': 'intermediate'}
    ]
    return jsonify({'users': users})


# A route just to make a token - doesnt save anywhere - I made this to create my hard coded token.
@app.route('/login', methods=['GET']) 
def login_user():
    token = jwt.encode({'user_id' : 9001, 'username' : 'Dosk3n', 'level' : 'master'}, app.config['SECRET_KEY'], "HS256")
    return jsonify({'token' : token})