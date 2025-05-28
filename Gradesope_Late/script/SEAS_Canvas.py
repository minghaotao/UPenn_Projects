import requests
import json
import csv


class Canvas:
    def __int__(self, instance):
        self.instance = instance

    def get_token(self=None):

        with open('/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/script/cred.json', 'r') as f:
            cred = json.load(f)

        return cred

    server_url = {'LPS_Production': 'https://canvas.upenn.edu/', 'LPS_Test': 'https://upenn.test.instructure.com/'}

    # token = get_token()

    def headers(self):
        token = self.get_token()
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(token[f'{self.instance}'])}
        return headers

    def post_submission_time(self, course_id, assignment_id, user_id, submission_time):
        submisson_times = '{}/api/v1/courses/{}/assignments/{}/submissions'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id)

        playload = {'submission[user_id]': user_id, 'submission[submitted_at]': submission_time,
                    'submission[submission_type]': 'basic_lti_launch',
                    'submission[url]': 'https://www.gradescope.com/auth/lti/callback'}

        r = requests.post(submisson_times, headers=self.headers(), params=playload)

        if r.status_code == 201:
            return json.dumps(r.json(), indent=4)
        else:
            raise Exception(f'{r.status_code},{r.text}')

    def post_assignment_grade(self, course_id, assignment_id, student_id, post_grade):

        assignment_grade = '{}/api/v1/courses/{}/assignments/{}/submissions/sis_user_id:{}'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id, student_id)

        playload = {'submission[posted_grade]': post_grade}

        r = requests.put(assignment_grade, headers=self.headers(), params=playload)

        if r.status_code == 200:
            return json.dumps(r.json(), indent=4)
        else:
            raise Exception(f'{r.status_code},{r.text}')

    def get_assignment_grades(self, course_id, assignment_id):

        student_grade = '{}/api/v1/courses/{}/assignments/{}/submissions'.format(
            self.server_url[f'{self.instance}'],
            course_id, assignment_id)

        r = requests.get(student_grade, headers=self.headers())

        if r.status_code == 200:
            return json.dumps(r.json(), indent=4)
            # return r.json()

        else:
            raise Exception(f'{r.status_code},{r.text}')


if __name__ == '__main__':
    canvas = Canvas()
    canvas.instance = 'LPS_Production'
    # print(canvas.post_submission_time(1654595, 10469300, 6104984, '2022-09-10T23:16:02Z'))
    # print(canvas.post_assignment_grade(1654595,10469300,45755436,100))

    print(canvas.get_assignment_grades(1654595, 10469300))
