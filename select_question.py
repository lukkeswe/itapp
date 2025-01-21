import random
import mysql.connector

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
    'database'  : 'itapp'
}

def select(year, option):
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
            random_question = result[random_number]
            #print(random_question)
            
            data['question'] = random_question[1]
            data['answer'] = random_question[2]
            
            cursor.execute(f"SELECT * FROM options WHERE question_id = '{random_question[3]}'")
            options = cursor.fetchall()
            
            aiue = ['a', 'i', 'u', 'e']
            for i, option in enumerate(options):
                raw = option[2]
                for item in rep_list:
                    if item in raw:
                        raw = raw.replace(item, "")
                data[aiue[i]] = raw
        else:
            print("no questions in table")
            return "error"
    else:
        print("no option")
        return "error"
                
    return data

print(select(None, 'random'))