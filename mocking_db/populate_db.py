import random
import traceback
import requests
from faker import Faker
from requests.exceptions import HTTPError
import os

NR_JOBS_PER_CATEGORY = 30
NR_PRODUCTS_PER_CATEGORY = 30
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
            print(f"Categories: HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Categories: Other error occurred: {err}")
        else:
            new_category_id = json_response['location'].rsplit('/', 1)[1]
            print(f"Success! Category location: {json_response.get('location', 'not created')}")
            add_jobs(new_category_id)
            add_products(new_category_id)


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
            print(f"Jobs: HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Jobs: Other error occurred: {err}")
        else:
            new_job_id = json_response['location'].rsplit('/', 1)[1]
            add_biddings(new_job_id)
            add_projects(new_job_id, job_object['user_email'])
            # attachments
            add_files(job_id=new_job_id, user_email=job_object['user_email'])


def add_biddings(job_id):
    uri = '/biddings/'
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
            print(f"Biddings: HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Biddings: Other error occurred: {err}")


def add_projects(job_id, employer_email):
    uri = '/projects/'

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
            print(f"Projects: HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Projects: Other error occurred: {err}")
        else:
            new_project_id = json_response['location'].rsplit('/', 1)[1]
            # delivered assets by freelancer
            add_files(project_id=new_project_id, user_email=employer_email, job_id=job_id)


def add_products(category_id):
    uri = '/marketplace/'

    for _ in range(random.randint(0, NR_PRODUCTS_PER_CATEGORY)):
        try:
            product_obj = {

                "user_email": faker.free_email(),
                "category_id": category_id,
                "name": faker.sentence(nb_words=random.randint(4, 10)),
                "description": faker.text(max_nb_chars=random.randint(100, 400)),
                "price": round(random.uniform(10, 10000), 2)

            }
            if random.choice([0, 1]) == 1:
                product_obj['partner_email'] = faker.free_email()
            response = requests.post(api_url + uri, json=product_obj)
            json_response = response.json()
            response.raise_for_status()

        except HTTPError as http_err:
            print(f"Products: HTTP error occurred: {http_err}")
            print(json_response)
        except Exception as err:
            print(f"Products: Other error occurred: {err}")
        else:
            new_product_id = json_response['location'].rsplit('/', 1)[1]
            # product assets
            add_files(product_for_sale_id=new_product_id)


def choose_random_files(directory):
    return random.choices(
        [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])


def add_files(job_id=None, project_id=None, product_for_sale_id=None, user_email=None):
    root_directory = '../mocking_db/'
    directories = ['archives', 'images', 'text_files']
    for directory in directories:
        directory_relative_path = root_directory + directory
        random_files = choose_random_files(directory_relative_path)
        for file in random_files:
            try:
                with open(file, 'rb') as upload_file:
                    files_param = dict(file=upload_file)
                    file_type = os.path.splitext(file)[1]
                    file_info = {'file_name': os.path.basename(file), 'file_type': file_type}

                    # project delivered asset
                    if job_id is not None and project_id is not None and user_email is not None:
                        uri = '/files/projectAssets/'
                        file_info['job_id'] = job_id
                        file_info['employer_email'] = user_email
                        file_info['project_id'] = project_id
                        file_info['message'] = faker.sentence(nb_words=random.randint(4, 100))

                    # job attachment
                    elif job_id is not None and user_email is not None:
                        uri = '/files/attachments/'
                        file_info['job_id'] = job_id
                        file_info['user_email'] = user_email
                    # product asset
                    elif product_for_sale_id is not None and file_type in ['.zip', '.rar', '.tar', '.png', '.jpg',
                                                                           '.jpeg']:
                        uri = '/files/productAssets/'
                        if file_type not in ['.zip', '.rar', '.tar']:
                            file_info['asset_type'] = 'image'
                        else:
                            file_info['asset_type'] = 'archive'
                        file_info['project_for_sale_id'] = product_for_sale_id
                    else:
                        print('Invalid request for uploading files')
                        return

                    response = requests.post(api_url + uri, files=files_param, params=file_info)
                    json_response = response.json()
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f"Files: HTTP error occurred: {http_err}")
                print(json_response)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    add_categories()
