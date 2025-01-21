import scraping
import mysql.connector

def scrape(year):
    data = []

    for i in range (1, 81):
        #year = "2menjo"
        question_id = year + str(i)
        item = scraping.scrape(f'https://www.fe-siken.com/kakomon/{year}/q{i}.html')
        item['id'] = question_id
        data.append(item)

    # print("data: ", data)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tvtittaren",
        database="itapp"
    )

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