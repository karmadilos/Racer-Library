# -- coding: utf-8 --
from flask import Flask, render_template, url_for, jsonify, session, request, redirect
import pymysql

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db_conn = pymysql.connect(
                user='root',  
                host='127.0.0.1',
                host='azure@elice-kdt-ai-track-vm-racer-12.koreacentral.cloudapp.azure.com',
                # password='blasy20159', 
                db='libraryuser', 
                charset='utf8',
                autocommit=True
)
db_cursor = db_conn.cursor()
# 시작 페이지
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # 회원가입 정보(이름, 이메일, 비밀번호)를 받음
        name = request.form['username']
        email = request.form['useremail']
        passwd = request.form['password']

        sql = "SELECT email FROM user"
        db_cursor.execute(sql)
        results = db_cursor.fetchall()
        # 이메일이 존재하는 경우 return 해준다.
        for result in results:
            print(result[0])
            if result[0] == email:
                return "이미 가입된 회원입니다."

        # 회원정보 DB에 추가
        sql = """
        INSERT INTO user(username, email, passwd) 
        VALUES('%s', '%s', '%s')
        """ % (str(name), str(email), str(passwd))
        db_cursor.execute(sql)
        db_conn.commit() 
        return redirect(url_for('login'))
    else:
        return render_template('register.html')
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 정보 받음
        email = request.form['useremail']
        passwd = request.form['password']
        
        sql = "SELECT email, passwd FROM user WHERE email = '%s'" % (email)
        db_cursor.execute(sql)
        result = db_cursor.fetchone()
        # 이메일, 비밀번호가 일치하지 않는 경우에 따라 조건으로 분류
        if result is not None:
            if result[1] == passwd:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                return '비밀번호가 틀립니다.'
        else:
            return '이메일이 없습니다.'
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    # 세션값을 False로 바꿔주고 홈으로 이동
    session['logged_in'] = False
    return render_template('index.html')

# 앱 실행
if __name__ == '__main__':
    # print("test", flush=True)
    app.run('0.0.0.0', port=80, debug = True)
    # app.run(debug = True)