import random
import mysql.connector
import os
import re

rep_list = [
    "</span>",
    '<span id="select_a">',
    '<span id="select_i">',
    '<span id="select_u">',
    '<span id="select_e">'
]

db_config = {
    'host'      : 'localhost',
    'user'      : 'root',
    'password'  : 'tvtittaren',
    'database'  : 'itdb'
}

IMAGE_FOLDER = os.path.join("static", "img")
app_root = os.path.dirname(os.path.abspath(__file__))

def getImage(year, question):
    filename = str(question) + ".png"
    relative_path = os.path.join(IMAGE_FOLDER, str(year), str(filename))
    absolute_path = os.path.join(app_root, relative_path)
    print("path:", absolute_path)
    if os.path.isfile(absolute_path):
        return True
    return False

def getNumber(question_id):
    last_two = str(question_id[-2:])
    cleaned_id = re.sub(r"[^0-9]", "", last_two)
    return cleaned_id

def select(year, option):
    if year is None:
        year = "31_haru"
    # 戻り値のオブジェクトを設計する
    data = {
        'question'  : None,
        'answer'    : None,
        'a'         : None,
        'i'         : None,
        'u'         : None,
        'q_image'   : None,
        'a_image'   : None,
        'i_image'   : None,
        'u_image'   : None,
        'e_image'   : None
    }
    # データベースに繋がる
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(err)
        return "ERROR"
    # ランダムの問題が欲しい場合
    if option == "random":
        if year == None:
            query = "SELECT * FROM questions"
            cursor.execute(query)
        else:
            query = "SELECT * FROM questions WHERE question_id LIKE %s"
            search_term = f"%{year}%"
            #print(query, (search_term,))
            cursor.execute(query, (search_term,))
        result = cursor.fetchall()
        if len(result) > 0:
            legnth = len(result) - 1
            random_number = random.randint(0, legnth)
            question = result[random_number]
        else:
            print("no questions in table")
            return "error"
    elif option == "specific":
        query = "SELECT * FROM questions WHERE question_id = %s"
        cursor.execute(query, (year, ))
        result = cursor.fetchall()
        question = result[0]
    else:
        print("no option")
        return "error"
    
    data['question'] = question[1]
    data['answer'] = question[2]
    data['id'] = question[3]
    
    cursor.execute(f"SELECT * FROM options WHERE question_id = '{question[3]}'")
    options = cursor.fetchall()
    
    question_number = getNumber(data['id'])
    if int(question_number) < 10:
        question_number = "0" + str(question_number)
    print("q number:", question_number)
    
    first_half = str(year[:-2])
    second_half = str(year[-2:])
    
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for number in numbers:
        second_half = second_half.replace(number, "")
    
    actual_year = str(first_half) + str(second_half)
    print("year:", actual_year)
        
    if getImage(actual_year, question_number):
        data['q_image'] = "img/" + actual_year + "/" + question_number + ".png"
    
    aiue = ['a', 'i', 'u', 'e']
    for i, option in enumerate(options):
        raw = option[2]
        for item in rep_list:
            if item in raw:
                raw = raw.replace(item, "")
        if "src=" in raw:
            if getImage(actual_year, str(question_number) + aiue[i]):
                key = aiue[i] + "_image"
                data[key] = "img/" + actual_year + "/" + question_number + aiue[i] + ".png"
                raw = " "
        data[aiue[i]] = raw
        
    for item in data.items():
        print(item)
    return data          
    

print(select(None, 'random'))