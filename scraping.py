import requests
from bs4 import BeautifulSoup


def scrape(url):
    # ページのHTMLを取得
    response = requests.get(url)

    # レスポンスのHTMLを解析する
    soup = BeautifulSoup(response.text, "lxml")

    question = soup.find(id = "mondai")

    mondai_text = question.get_text()    

    options = {"a": "", "i": "", "u": "", "e": ""}
    
    options["a"] = soup.find(id = "select_a")
    options["i"] = soup.find(id = "select_i")
    options["u"] = soup.find(id = "select_u")
    options["e"] = soup.find(id = "select_e")

    answer = soup.find(id = "answerChar")

    answerChar = answer.get_text()

    print(question)
    print(answer)
    
    data = {
        "question": mondai_text,
        "options": options,
        "answer": answerChar
    }
    return data