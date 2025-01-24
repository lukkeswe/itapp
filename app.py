from flask import Flask, render_template, redirect, url_for, session, request
import select_question as sq
import mysql.connector
import it
import picdown
import random as rand
import os
import re

app = Flask(__name__,
            static_folder='static',
            static_url_path="")

app.secret_key = 'supersecretkey'

IMAGE_FOLDER = os.path.join("static", "img")
app.config["IMAGE_FOLDER"] = IMAGE_FOLDER

app_root = os.path.dirname(os.path.abspath(__file__))
print("path:", app_root)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    if session.get('loginMsg') is None:
        session['loginMsg'] = ""
    return render_template('login.html', msg=session['loginMsg'])

@app.route('/sign-in', methods=['POST'])
def sign_in():
    username = request.form['name']
    password = request.form['password']
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tvtittaren",
            database="itapp"
        )
        cursor = conn.cursor()
        
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username, ))
        result = cursor.fetchall()
        
        print(f"Checking if {username} exist:")
        if len(result) == 0:
            session['loginMsg'] = "ユーザー名が存在していません。"
            return redirect(url_for('login'))
        exist = False
        for item in result:
            if item[1] == username:
                exist = True
                actualPassword = item[3]
                userData = item
                break
        if exist == False:
            print("don't exist")
            print("Redirecting")
            session['loginMsg'] = "ユーザー名が存在していません。"
            return redirect(url_for('login'))
        print("exist")
        
        print("Checking if password match:")
        if password != actualPassword:
            print("does not match")
            print("Redirecting")
            session['loginMsg'] = "パスワードが間違いです"
            return redirect(url_for('login'))
        print("match")
        
        session['username'] = username
        session['userId']   = userData[0]
        
        print("Fetching experience data:")
        sql = "SELECT * FROM experience WHERE username = %s"
        cursor.execute(sql, (username, ))
        result = cursor.fetchall()
        
        if result == 0:
            print("ERROR! : no experience data was found")
            session['loginMsg'] = "エラー：ユーザーのデータが見つかりませんでした"
            return redirect(url_for('login'))
        print("ok")
        for item in result:
            if item[1] == username:
                experienceData = item
        
        session['xp']       = experienceData[2]
        session['qcount']   = experienceData[3]
        session['highscore']= experienceData[4]
        
        cursor.close()
        conn.close()
        return redirect(url_for('toi'))
        
    except mysql.connector.Error as err:
        print(err)
        return redirect(url_for('login'))

@app.route('/random')
def random():
    data = sq.select(None, 'random')
    
    session['question'] = data['question']
    session['a'] = data['a']
    session['i'] = data['i']
    session['u'] = data['u']
    session['e'] = data['e']
    session['answer'] = data['answer']
    print("answer: ", session['answer'])
    
    session['msg'] = ""
    
    return redirect(url_for('toi'))

def getImage(year, question):
    filename = str(question) + ".png"
    relative_path = os.path.join(app.config['IMAGE_FOLDER'], year, filename)
    absolute_path = os.path.join(app_root, relative_path)
    if os.path.isfile(absolute_path):
        return True
    return False

def getNumber(question_id):
    last_two = str(question_id[-2:])
    cleaned_id = re.sub(r"[^0-9]", "", last_two)
    print("id:", cleaned_id)
    return cleaned_id

@app.route('/by-year', methods=['POST'])
def by_year():
    year = request.form['year']
    if int(year) < 21:
        if int(year) == 1:
            qYear = "01_aki"
        else:
            qYear = "0" + str(year) + "_menjo"
        data = sq.select(qYear, "random")
    else:
        qYear1 = str(year) + "_aki"
        qYear2 = str(year) + "_haru"
        data1 = sq.select(qYear1, "random")
        data2 = sq.select(qYear2, "random")
        coin = rand.randint(0, 1)
        if coin == 1:
            data = data1
            qYear = qYear1
        else:
            data = data2
            qYear = qYear2
            
    question_number = getNumber(data["id"])
    if int(question_number) < 10:
        question_number = "0" + str(question_number)
    
    if getImage(qYear, question_number):
        session["src"] = "img/" + qYear + "/" + question_number + ".png"
        print("src:", session["src"])
    else:
        if session.get('src'):
            session.pop('src')
        
    session['question'] = data['question']
    session['a'] = data['a']
    session['i'] = data['i']
    session['u'] = data['u']
    session['e'] = data['e']
    session['answer'] = data['answer']
    session['questionId'] = data['id']
    print("answer: ", session['answer'])
    
    session['msg'] = ""
    
    return redirect(url_for('toi'))
    
@app.route('/toi')
def toi():
    data = {}
    
    if session.get('username') is not None:
        data['username'] = session['username']
        data['userId'] = session['userId']
        data['xp'] = session['xp']
        data['qcount'] = session['qcount']
        data['highscore'] = session['highscore']
    
    if session.get('question') is not None:
        data['question'] = session['question']
        data['a'] = session['a']
        data['i'] = session['i']
        data['u'] = session['u']
        data['e'] = session['e']
        if session.get("src") is not None:
            data['src'] = session['src']
        
    if session.get('msg') is None:
        session['msg'] = ""
    data['msg'] = session['msg']
    return render_template("toi.html", data=data)

@app.route('/answer', methods=["POST"])
def answer():
    db_config = {
        'host'      : 'localhost',
        'user'      : 'root',
        'password'  : 'tvtittaren',
        'database'  : 'itapp'
    }
    answer = request.form['answer']
    if answer == session['answer']:
        session['msg'] = "正解！"
        if session['qcount'] == 0:
            session['xp'] += 1
        else:
            session['xp'] += session['qcount']
        session['qcount'] += 1
        print("正解！")
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            if int(session['qcount']) >= int(session['highscore']):
                sql = "UPDATE experience SET xp = %s, qcount = %s, highscore = %s WHERE username = %s"
                cursor.execute(sql, (int(session['xp']), int(session['qcount']), int(session['qcount']), session['username']))
            else:
                sql = "UPDATE experience SET xp = %s, qcount = %s WHERE username = %s"
                cursor.execute(sql, (int(session['xp']), int(session['qcount']), session['username']))
            
            sql = "SELECT * FROM result WHERE username = %s"
            cursor.execute(sql, (session['username'], ))
            result = cursor.fetchall()
            sql = "INSERT INTO result (username, question_id, is_correct) VALUES (%s, %s, 1)"
            if result:
                for item in result:
                    if item[2] == session['questionId']:
                        sql = "UPDATE result SET is_correct = 1 WHERE username = %s AND question_id = %s"
                        break
                    sql = "INSERT INTO result (username, question_id, is_correct) VALUES (%s, %s, 1)"
            cursor.execute(sql, (session['username'], session['questionId']))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            session['msg'] = str(err)
            return redirect(url_for('toi'))
        return redirect(url_for('toi'))
    session['msg'] = "残念..."
    session['highscore'] = 0
    print("残念...")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "UPDATE experience SET qcount = 0 WHERE username = %s"
        cursor.execute(sql, (session['username'], ))
        
        sql = "SELECT * FROM result WHERE username = %s"
        cursor.execute(sql, (session['username'], ))
        result = cursor.fetchall()
        sql = "INSERT INTO result (username, question_id, is_correct) VALUES (%s, %s, 0)"
        if result:
            for item in result:
                if item[2] == session['questionId']:
                    sql = "UPDATE result SET is_correct = 0 WHERE username = %s AND question_id = %s"
                    break
                
        cursor.execute(sql, (session['username'], session['questionId']))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        session['msg'] = str(err)
        return redirect(url_for('toi'))
    return redirect(url_for('toi'))

@app.route('/sign-up')
def sign_up():
    session['signMsg'] = ""
    return render_template("signup.html", msg=session['signMsg'])

@app.route('/create-user', methods=['POST'])
def create_user():
    newUserName = request.form['name']
    newEmail    = request.form['email']
    newPassword = request.form['password']
    
    # 入力を確認する
    if len(newUserName) > 20 or len(newUserName) < 4:
        session['signMsg'] = "ユーザー名の入力エラー"
        return redirect(url_for('sign_up'))
    if len(newPassword) < 6:
        session['signMsg'] = "入力されたパスワードは短いです"
        return redirect(url_for('sign_up'))
    if len(newEmail) > 100 or len(newEmail) < 10:
        session['signMsg'] = "メールアドレスの入力エラー"
        return redirect(url_for('sign_up'))
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tvtittaren",
            database="itapp"
        )
        cursor = conn.cursor()
        
        # 新しいユーザー名もう存在しているかどうかを確認する
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (newUserName, ))
        result = cursor.fetchall()
        
        # 結果を確認する
        for item in result:
            if item[1] == newUserName:
                session['signMsg'] = "入力されたユーザー名もう存在しています。"
                return redirect(url_for('sign_up'))
            if item[2] == newEmail:
                session['signMsg'] = "入力されたメールアドレスもう存在しています。"
                return redirect(url_for('sign_up'))
        print("Creating user:")
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (newUserName, newEmail, newPassword))
        conn.commit()
        print("success")
        print(f"Creating 'experience' for {newUserName}:")
        sql = "INSERT INTO experience (username, xp, qcount, highscore) VALUES (%s, 0, 0, 0)"
        cursor.execute(sql, (newUserName, ))
        conn.commit()
        print("success")
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (newUserName, ))
        result = cursor.fetchall()
        print(result)
        userId = result[0][0]
        
        session['username'] = newUserName
        session['userId']   = userId
        session['xp'] = 0
        session['qcount'] = 0
        session['highscore'] = 0
        
        cursor.close()
        conn.close()
        return redirect(url_for('toi'))
    except mysql.connector.Error as err:
        print(err)
        return redirect(url_for('sign_up'))

@app.route('/download', methods=['POST'])
def download():
    adminpass = request.form['password']
    
    if adminpass == "superpass":
    
        years = [
            "04_menjo",
            "03_menjo",
            "02_menjo",
            "01_aki",
            "31_haru",
            "30_aki",
            "30_haru",
            "29_aki",
            "29_haru",
            "28_aki",
            "28_haru",
            "27_aki",
            "27_haru",
            "26_aki",
            "26_haru",
            "25_aki",
            "25_haru",
            "24_aki",
            "24_haru",
            "23_aki",
            "23_toku",
            "22_aki",
            "22_haru",
            "21_aki",
            "21_haru"
        ]
        
        for year in years:
            it.scrape(year)
        print("Finnished downloading data")
        print("----------------")
        print("Downloading pictures")
        
        for year in years:
            for i in range(1, 81):
                picdown.picture(f"https://www.fe-siken.com/kakomon/{year}/", i, year)
        
        return "Scraping successfull"
    return "password incorrect"

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')
    
app.run(debug=True)