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

def get_title(url):
    # Send a GET request
    response = requests.get(url)

    # Parse the HTML using 'lxml' (better at handling broken HTML)
    soup = BeautifulSoup(response.text, "lxml")

    # Find the table with class "qtable"
    table = soup.find("table", class_="qtable")

    # Extract all <tr> elements while filtering out headers
    if table:
        rows = table.find_all("tr")
        data = []
        for row in rows:
            # Skip rows that contain <th> (header rows) or class "h"
            if row.find("th") or "h" in row.get("class", []):
                continue

            # Extract <td> elements (without recursive=False)
            tds = row.find_all("td")

            # Ensure there are at least 2 <td> elements before extracting the second one
            if len(tds) >= 2:
                print(tds[1].get_text(strip=True))  # Print only the second <td>
                data.append(tds[1].get_text(strip=True))
        return data

    else:
        print("Table not found.")
        return []

def get_category(url):
    # Send a GET request
    response = requests.get(url)

    # Parse the HTML using 'lxml' (better at handling broken HTML)
    soup = BeautifulSoup(response.text, "lxml")

    # Find the table with class "qtable"
    table = soup.find("table", class_="qtable")

    # Extract all <tr> elements while filtering out headers
    if table:
        rows = table.find_all("tr")
        data = []
        for row in rows:
            # Skip rows that contain <th> (header rows) or class "h"
            if row.find("th") or "h" in row.get("class", []):
                continue

            # Extract <td> elements (without recursive=False)
            tds = row.find_all("td")

            # Ensure there are at least 2 <td> elements before extracting the second one
            if len(tds) >= 2:
                print(tds[2].get_text(strip=True))  # Print only the second <td>
                data.append(tds[2].get_text(strip=True))
        return data

    else:
        print("Table not found.")
        return []