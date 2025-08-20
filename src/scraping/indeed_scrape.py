import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

DB_PATH = "sqlite:///db/jobs.db"

def get_jobs():
    url = "https://vn.indeed.com/q-ai-engineer-vi%E1%BB%87c-l%C3%A0m.html?vjk=418b1c7ce88a63c7"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    jobs = []
    return response


if __name__ == "__main__":
    print(get_jobs())
