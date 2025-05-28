#####################################################################################################################
##
## Copyright (C) 2022-23 by Edward Tao
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## You are allowed to use, modify my code for your own projects.The user must clearly attribute the original authorship to Edward Tao
## and provide appropriate credit by prominently displaying the following notice in their project documentation, source code comments,
## and wherever the Code is utilized: "Original Code written by Edward Tao"
#####################################################################################################################

from Slack_bot import updated_slack_bot
import requests
import json
from datetime import datetime
from datetime import timedelta
from slacker import Slacker


def load_json():
    with open("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/main/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message):
    cred = load_json()["new_slack_bot_token"]
    CHANNEL_ID = "C04K5V2JF8D"
    headers = {"Authorization": f"Bearer {cred}", "Content-Type": "application/json"}
    # file_path = f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{message}.png'

    updated_slack_bot.post_message(message, CHANNEL_ID, headers)

class Canvas:
    def __int__(self, instance):
        self.instance = instance

    def get_token(self=None):

        with open('/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/script/cred.json', 'r') as f:
            cred = json.load(f)

        return cred

    server_url = {'LPS_Production': 'https://canvas.upenn.edu/', 'LPS_Test': 'https://upenn.test.instructure.com/'}

    def headers(self):
        token = self.get_token()
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(token[f'{self.instance}'])}
        return headers

    def post_assignment_grade(self, course_id, assignment_id, student_id, post_grade):

        assignment_grade = '{}/api/v1/courses/{}/assignments/{}/submissions/{}?per_page=200'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id, student_id)

        playload = {'submission[posted_grade]': post_grade}

        not_done = True
        while not_done:

            r = requests.put(assignment_grade, headers=self.headers(), params=playload)

            if r.status_code == 200:
                # print(json.dumps(r.json(), indent=4))
                print(f'{course_id} - {assignment_id} - {student_id} - 0')
            else:
                pass

            if 'next' in r.links.keys():
                assignment_grade = r.links['next']['url']

            else:
                not_done = False
                print(assignment_grade)

    def time_conversion(self, assignment_due):

        current_day = datetime.today()
        assignment_due = datetime.strptime(assignment_due, '%Y-%m-%dT%H:%M:%SZ') + timedelta(days=9)

        # print(current_day)
        print(assignment_due)

        if current_day > assignment_due:

            print('Assignment has passed 7 days')

            return True
        else:

            print('Assignment has not passed 7 days')
            return False

    def get_assignment_name_due_date(self, course_id, assignment_id):

        assignment_total_grade = '{}/api/v1/courses/{}/assignments/{}/date_details'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id)

        r = requests.get(assignment_total_grade, headers=self.headers())

        if r.status_code == 200:

            # print(r.json()["due_at"])

            return r.json()["due_at"]
        else:
            raise Exception(f'{r.status_code},{r.text}')

    def filter_assignments(self, course_id):

        assignment_ids = {}

        assignment_type = '{}/api/v1/courses/{}/assignments/?per_page=180'.format(
            self.server_url[f'{self.instance}'],
            course_id)

        r = requests.get(assignment_type, headers=self.headers())

        response = r.json()

        if isinstance(response, list):
            for data in response:
                print(data["name"])
                if isinstance(data, dict):
                    if (data.get('due_at') and data.get('graded_submissions_exist') is True) and (
                            data.get('submission_types') == ['external_tool']) and (
                            data['external_tool_tag_attributes']['content_id'] != 132820):

                        due_date = self.get_assignment_name_due_date(course_id, data["id"])

                        if self.time_conversion(due_date) is True:
                            # self.time_conversion(data['due_at']) is True)

                            # assignment_ids[data["name"]] = data["id"]

                            assignment_ids[data["id"]] = data["name"]
                        # print(data['due_at'])
                        # print(data["name"])
                else:
                    print(f"Expected a dictionary but got {type(data)}: {data}")
        else:
            print(f"Expected a list but got {type(response)}: {response}")

        print(assignment_ids)

        # return list(assignment_ids.values())

        return assignment_ids

    def get_assignment_grades(self, course_id, assignment_id):

        student_grade = '{}/api/v1/courses/{}/assignments/{}/submissions?per_page=100'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id)

        all_grades = []
        not_done = True
        while not_done:

            r = requests.get(student_grade, headers=self.headers())

            if r.status_code == 200:

                all_grades.extend(r.json())
                # return r.json()
            else:
                pass

            if 'next' in r.links.keys():
                student_grade = r.links['next']['url']
                print(student_grade)

            else:
                not_done = False
                print(student_grade)

        return all_grades

    def assign_zero(self, course_name, course_id):

        messgae = ""

        assignments = canvas.filter_assignments(course_id)

        for assignment, assignment_name in assignments.items():

            report = canvas.get_assignment_grades(course_id, assignment)

            for data in report:

                grade = data.get('grade')
                # print(data['grade'])

                if grade is None and data['excused'] is None:
                #
                # if data['grade'] is None and data['excused'] is False:
                    canvas.post_assignment_grade(course_id, assignment, data['user_id'], 0)

                    messgae += f"{assignment_name} - {data['user_id']} has been assigned to 0\n"

        if len(messgae) > 0:
            slack_bot(f'-------------------{course_name}-----------------')
            print(messgae)
            slack_bot(messgae)
        else:
            print("no updates")
            # slack_bot("No updates from Entering Zero Script", 'msg')


def main():
    course_lists = {'5910': 1831656, '5920': 1831659, }


    for course_name, course_id in course_lists.items():
        canvas.assign_zero(course_name, course_id)

        print(course_name)


if __name__ == '__main__':
    canvas = Canvas()
    canvas.instance = 'LPS_Production'
    main()

    # main(1655680, 10168856)
    # canvas.get_assignment_name_due_date(1803699, 12470519)

    # canvas.filter_assignments(1801591)
    # canvas.assign_zero('5910',1801591)
    # canvas.time_conversion('2024-07-5T03:59:00Z')
