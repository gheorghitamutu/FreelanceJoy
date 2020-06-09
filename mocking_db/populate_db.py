import requests
from requests.exceptions import HTTPError
from faker import Faker
import random

NR_JOBS_PER_CATEGORY = 30
NR_BIDDINGS_PER_JOB = 5
api_url = 'http://127.0.0.1:5000/api'
faker = Faker()


def add_categories():
    uri = '/categories/'
    category_names = ['Graphics & Design', 'Music & Audio', 'Programming & Tech', 'Video & Animation',
                      'Writing & Translation', 'Business']

    for category_name in category_names:
        try:
            category_object = {'name': category_name}
            response = requests.post(api_url + uri, json=category_object)
            json_response = response.json()
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            new_category_id = json_response['location'].rsplit('/', 1)[1]
            print(f"Success! Category location: {json_response.get('location', 'not created')}")
            add_jobs(new_category_id)


def add_jobs(category_id):
    uri = '/jobs/'

    for _ in range(random.randint(10, NR_JOBS_PER_CATEGORY)):
        try:
            job_object = {
                "user_email": faker.free_email(),
                "title": faker.sentence(nb_words=random.randint(4, 10)),
                "description": faker.text(max_nb_chars=random.randint(100, 400)),
                "payment": round(random.uniform(10, 10000), 2),
                "category_id": category_id
            }
            response = requests.post(api_url + uri, json=job_object)
            json_response = response.json()
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            new_job_id = json_response['location'].rsplit('/', 1)[1]
            add_biddings(new_job_id)
            add_projects(new_job_id)


def add_biddings(job_id):
    uri = '/biddings/'
    ids = []
    for _ in range(random.randint(0, NR_BIDDINGS_PER_JOB)):
        try:
            bidding_obj = {
                "freelancer_email": faker.free_email(),
                "message": faker.text(max_nb_chars=random.randint(100, 1000)),
                "job_id": job_id
            }
            response = requests.post(api_url + uri, json=bidding_obj)
            json_response = response.json()
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Other error occurred: {err}")



def add_projects(job_id):
    uri = '/projects/'
    ids = []

    if random.choice([1, 0, 0, 0]) == 1:
        try:
            project_obj = {
                "deadline": faker.date_time_between(start_date='+10d', end_date='+30d').isoformat(),
                "freelancer_email": faker.free_email(),
                "job_id": job_id
            }
            response = requests.post(api_url + uri, json=project_obj)
            json_response = response.json()
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Other error occurred: {err}")



if __name__ == '__main__':
    add_categories()
