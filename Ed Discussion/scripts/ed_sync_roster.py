import requests
import json
import ed_main

course_lists = ed_main.courses

headers = {'Authorization': 'Bearer ' + ''}


def course_list():
    for course, ed_id in course_lists.items():
        ed_id = ed_id.split('/')
        ed_id = ed_id[5]

        course_url = f'https://us.edstem.org/api/courses/{ed_id}/sync_roles'

        print(course)
        sync_roster(course_url)


def sync_roster(course_url):
    r = requests.post(course_url, headers=headers)

    if r.status_code == 200:
        print(json.dumps(r.json(), indent=4))
    else:
        raise Exception(f'{r.status_code},{r.text}')


#
if __name__ == '__main__':
    # sync_roster()
    course_list()
