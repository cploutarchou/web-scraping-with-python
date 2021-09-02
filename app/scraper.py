import datetime
import logging
import time

import graypy
import requests
from bs4 import BeautifulSoup

from models import insert_entry, Connection

"""
   Setup the logger
   """
logger = logging.getLogger('ScraperCronJob')
logger.setLevel(logging.INFO)

handler = graypy.GELFTCPHandler('172.21.0.35', 12201)
logger.addHandler(handler)
BASE_URL = "https://stackoverflow.com"


# the function to extract the last page of the pagination_group
def fetch_questions(page: int = 1) -> list:
    questions_url = f"{BASE_URL}/questions?tab=active&page={page}"
    logger.info(f"Trying to fetch questions from url: {questions_url}")
    try:
        # get the response of the url

        result = requests.get(questions_url)

        # make a BeautifulSoup code from raw html text data
        soup = BeautifulSoup(result.text, "html.parser")

        # get the <div> tag part with class="pagination" from html
        pagination = soup.find("div", {"id": "questions"})

        # get all the <a> tags in pagination <div> tag as the python list
        questions = pagination.find_all('div', {'class': "question-summary"})
        # add all questions in a list to
        page_questions = [question for question in questions]
        return page_questions

    except requests.exceptions.ConnectionError as e:
        logger.info(f"Something went wrong unable to fetch data from url {questions_url}")
        if "Max retries" in e.__str__():
            logger.info("Waiting 1m max retries error appears.")
            time.sleep(60)
            try:
                fetch_questions(page=page)
            except requests.exceptions.ConnectionError as e:
                raise e


# the function to extract the question data
def extract_data(html):
    question = html
    tags = html.find_all("a", {"class": "post-tag flex--item"})
    tags = [tag.text for tag in tags]
    post_id = int(question['id'].split('-')[2])
    count = str(question.find("span", {"class": "vote-count-post"}).text)
    answers = int(question.find("div", {"class": "status"}).find("strong").text)
    view = str(question.find("div", {"class": "views"}).text.strip().split("views")[0]).upper().strip()
    print(view)
    views = convert_str_to_number(view)
    question_hyperlink = f"{BASE_URL}{question.find('a', {'class': 'question-hyperlink'})['href']}"
    title = question.find('a', {'class': 'question-hyperlink'}).text
    content = question.find('div', {'class': 'excerpt'}).text
    content = " ".join(content.split())
    user = question.find('div', {'class': 'user-details'}).find('a').text
    asked = question.find('span', {'class': 'relativetime'})['title'][0:-1]
    # convert date string to datetime object
    asked = datetime.datetime.strptime(asked, '%Y-%m-%d %H:%M:%S')
    # fix text spacing

    payload = {
        "post_id": post_id,
        'title': title,
        'user': user,
        'created_at': asked,
        'votes': count,
        'answers': answers,
        'views': views,
        'url': question_hyperlink,
        'content': content,
        'categories': tags
    }
    return payload


def execute_job(pages: int = 1):
    final_data = []
    if pages == 1:
        logger.info(f"Gathering data . Page No{pages}")
        questions = fetch_questions()
        page_questions = [extract_data(question) for question in questions]

        final_data = page_questions
    else:
        for n in range(1, pages + 1):
            logger.info(f"Gathering data . Page no{n}")
            questions = fetch_questions(page=n)
            time.sleep(15)
            page_questions = [extract_data(question) for question in questions]
            final_data.extend(page_questions)
    logger.info(f"Found {len(final_data)} questions.")

    logger.info("Starting update database entries")
    failed_jobs = {}
    failed_jobs_index = 0
    for i in final_data:
        res = insert_entry(data=i)
        if res is None:
            logger.error(f"Unable to insert entry. Data: {i}")
            failed_jobs[failed_jobs_index] = i
            failed_jobs_index += 1
        elif res is False:
            continue

    if len(failed_jobs) > 0:
        for key, val in failed_jobs.items():
            client.__enter__()
            res = insert_entry(data=val)
            if res is None:
                failed_jobs.pop(key)
            elif res is False:
                continue
    if len(failed_jobs) > 0:
        logger.info(f"Process update database entries . Completed . Failed jobs: {len(failed_jobs)}")
        logger.error(f"Failed jobs data : {failed_jobs}")
        return False

    else:
        return True


def convert_str_to_number(x):
    total_likes = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_likes = int(x)
    else:
        if len(x) > 1:
            total_likes = int(float(x[:-1])) * num_map.get(x[-1].upper(), 1)
    return int(total_likes)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    client = Connection()
    client.__enter__()
    logger.info(f"Starting Updating Database .Start time: {start_time}")

    if execute_job(500) is True:
        end = datetime.datetime.now()
        logger.info(
            f"Updating Database jobs has been successfully completed . Execution time: {end - start_time}")
    else:
        logger.info("Something going Wrong. Unable to update database")

    client.__exit__()
    exit(0)
