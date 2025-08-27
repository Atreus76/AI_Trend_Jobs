import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

DB_PATH = r"sqlite:///db/jobs.db"
engine = create_engine(DB_PATH)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                posted TEXT,
                url TEXT UNIQUE,
                description TEXT
            )
        """))
        conn.commit()

def scrape_python_jobs():
    url = "https://www.python.org/jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    jobs = []
    for job in soup.select("ol.list-recent-jobs li"):
        title_elem = job.select_one("h2 a")
        title = title_elem.text.strip() if title_elem else ""
        company_elem = job.select_one("span.listing-company-name")
        company = company_elem.text.strip() if company_elem else ""
        location_elem = job.select_one("span.listing-location")
        location = location_elem.text.strip() if location_elem else ""
        posted_elem = job.select_one("span.listing-posted")
        posted = posted_elem.text.strip() if posted_elem else ""
        job_url = "https://www.python.org" + str(title_elem["href"]) if title_elem and title_elem.has_attr("href") else ""

        # fetch description
        job_html = requests.get(job_url).text
        job_soup = BeautifulSoup(job_html, "lxml")
        desc_elem = job_soup.select_one("div.job-description")
        description = desc_elem.get_text(" ", strip=True) if desc_elem else ""

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "posted": posted,
            "url": job_url,
            "description": description
        })
    return jobs

def save_jobs(jobs):
    with engine.begin() as conn:
        for job in jobs:
            try:
                conn.execute(text("""
                    INSERT INTO jobs (title, company, location, posted, url, description)
                    VALUES (:title, :company, :location, :posted, :url, :description)
                """), job)
            except Exception:
                # Skip duplicates
                continue

if __name__ == "__main__":
    init_db()
    jobs = scrape_python_jobs()
    save_jobs(jobs)
    print(f"Saved {len(jobs)} jobs into database.")
