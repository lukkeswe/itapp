import scraping
import mysql.connector
import db_config

def scrape(year):
    data = []

    for i in range (1, 81):
        #year = "2menjo"
        question_id = year + str(i)
        item = scraping.scrape(f'https://www.fe-siken.com/kakomon/{year}/q{i}.html')
        item['id'] = question_id
        data.append(item)

    # print("data: ", data)

    conn = mysql.connector.connect(**db_config.config)

    cur = conn.cursor()

    for mondai in data:
        question = mondai['question']
        answer = mondai['answer']
        id = mondai['id']
        
        sql = """
            INSERT INTO questions (
            question_text, 
            correct_answer, 
            question_id
            ) VALUES (
            %s, %s, %s
            ) 
        """
        cur.execute(sql, (question, answer, id))
        conn.commit()

        for key, value in mondai['options'].items():
            is_correct = 0
            match answer:
                case "ア":
                    if key == "a":
                        is_correct = 1
                case "イ":
                    if key == 'i':
                        is_correct = 1
                case "ウ":
                    if key == 'u':
                        is_correct = 1
                case "エ":
                    if key == 'e':
                        is_correct = 1

            sql = """
                INSERT INTO options (
                question_id,
                option_text,
                is_correct
                ) VALUES (
                %s, %s, %s
                ) 
            """
            cur.execute(sql, (str(id), str(value), is_correct))
            conn.commit()

    cur.close()
    conn.close()
    
def add_title(year):
    data = scraping.get_title("https://www.fe-siken.com/kakomon/" + year + "/")
    
    try:
        conn = mysql.connector.connect(**db_config.config)

        cur = conn.cursor()
        for i, title in enumerate(data):
            sql = "UPDATE questions SET title = %s WHERE question_id = %s"
            cur.execute(sql, (title, str(year + str(i + 1))))
        
        conn.commit()
        cur.close()
        conn.close()
            
        
    except mysql.connector.Error as err:
        print(err)

def add_category(year):
    data = scraping.get_category("https://www.fe-siken.com/kakomon/" + year + "/")
    
    try:
        conn = mysql.connector.connect(**db_config.config)

        cur = conn.cursor()
        for i, title in enumerate(data):
            sql = "UPDATE questions SET category = %s WHERE question_id = %s"
            cur.execute(sql, (title, str(year + str(i + 1))))
        
        conn.commit()
        cur.close()
        conn.close()
            
        
    except mysql.connector.Error as err:
        print(err)