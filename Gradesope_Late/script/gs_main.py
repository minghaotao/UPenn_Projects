import pandas as pd
import requests
from SEAS_Canvas import Canvas
# from Canvas_API.SAS_Canvas import Canvas
import json
from slacker import Slacker
from datetime import datetime
import gradescope
from datetime import timedelta
import time
import send_email
import logging
import datetime
from Slack_bot import updated_slack_bot


def log_error_message(msg):
    logging.basicConfig(filename='error.txt', level=logging.ERROR, format='%(asctime)s %(message)s')
    logging.error(msg)


def load_json():
    with open("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/main/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message):
    cred = load_json()["new_slack_bot_token"]
    CHANNEL_ID = ""
    headers = {"Authorization": f"Bearer {cred}", "Content-Type": "application/json"}
    # file_path = f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{message}.png'

    updated_slack_bot.post_message(message, CHANNEL_ID, headers)


def get_student_id(student_id):
    canvs_id = '{}/api/v1/users/sis_user_id:{}'.format(canvas.server_url[f'{canvas.instance}'],
                                                       student_id)

    r = requests.get(canvs_id, headers=canvas.headers())

    if r.status_code == 200:

        # return json.dumps(r.json(), indent=4)
        # print(r.json()['id'])
        return r.json()['id']
    else:
        raise Exception(f'{r.status_code},{r.text}')
    # return canvas.get_canvas_id(student_id)


def check_student_enrollment(student_id, course_id):
    uselr_enrollmenets = '{}/api/v1/users/sis_user_id:{}/enrollments'.format(canvas.server_url[f'{canvas.instance}'],
                                                                             student_id)
    playload = {'state[]': 'active'}

    r = requests.get(uselr_enrollmenets, headers=canvas.headers(), params=playload)

    if r.status_code == 200:

        for data in r.json():
            if course_id == data["course_id"]:
                return True
            else:
                return False
    else:

        raise Exception(f'{r.status_code},{r.text}')


def check_submission_time(course_id, assignment_id, user_id):
    get_submission_time = '{0}/api/v1/courses/{1}/assignments/{2}/submissions/sis_user_id:{3}'.format(
        canvas.server_url[f'{canvas.instance}'],
        course_id, assignment_id, user_id)

    r = requests.get(get_submission_time, headers=canvas.headers())

    if r.status_code == 200:

        timestamp = r.json()["submitted_at"]

        if timestamp is not None:

            daylight_saving = '2025-03-10T00:00:00Z'

            if datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ') > datetime.datetime.strptime(daylight_saving,
                                                                                                        '%Y-%m-%dT%H:%M:%SZ'):

                est_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=4)

                # print(est_timestamp)
                # print(timestamp)
                return est_timestamp
            else:
                est_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=5)

                # print(est_timestamp)
                # print(timestamp)
                return est_timestamp

        else:

            # print(timestamp)
            return timestamp
    else:
        raise Exception(f'{r.status_code},{r.text}')


def upload_submission_time(course_id, assignment_id, user_id, submission_time):
    submisson_times = '{}/api/v1/courses/{}/assignments/{}/submissions'.format(
        canvas.server_url[f'{canvas.instance}'],
        course_id, assignment_id)

    student_canvas_id = get_student_id(user_id)

    # print(student_canvas_id)

    playload = {'submission[user_id]': student_canvas_id, 'submission[submitted_at]': submission_time,
                'submission[submission_type]': 'basic_lti_launch',
                'submission[url]': 'https://www.gradescope.com/auth/lti/callback'}

    r = requests.post(submisson_times, headers=canvas.headers(), params=playload)

    if r.status_code == 201:

        # print(json.dumps(r.json(), indent=4))
        print(f'{course_id} - {assignment_id} - {user_id} - {submission_time} - uploaded')
        return json.dumps(r.json(), indent=4)
    else:
        raise Exception(f'{r.status_code},{r.text}')


def send_emails(message):
    today = datetime.date.today().strftime("%m/%d/%Y")
    sender_email_address = "idd@seas.upenn.edu"
    recipient_email = "edtao@seas.upenn.edu,asavoth@seas.upenn.edu,aammarah@seas.upenn.edu,drewhop@seas.upenn.edu,masseybr@seas.upenn.edu"
    subject = f"GS Late Submission Report-{today}"
    message = message
    attachment_file_path = '/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/late_files/late_submissions.csv'

    send_email.send_email_func(sender_email_address, recipient_email, subject, message, attachment_file_path)


def access_files():
    df = pd.read_csv("/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/late_files/late_submissions.csv")

    df = df[df["Lateness (H:M:S)"] > '01:00:00']

    # print(type(df["Lateness (H:M:S)"]))

    message = ""
    error = "*********Error Log*********\n"

    for index, row in df.iterrows():

        # print(row['Canvas_course_id'], row['assignment_id'], row['SID'])
        # student_submission_time = check_submission_time(row['Canvas_course_id'], row['assignment_id'], row['SID'])
        #
        # print(student_submission_time)

        try:
            student_submission_time = check_submission_time(row['Canvas_course_id'], row['assignment_id'], row['SID'])

            new_time = datetime.datetime.strptime(row['submission_time'], '%Y-%m-%d %H:%M:%S')
            # print(new_time)
            if student_submission_time is None or student_submission_time != new_time:

                upload_submission_time(row['Canvas_course_id'], row['assignment_id'], row['SID'],
                                       row['submission_time'])

                row = f" {row['student_name']} - {row['assignment_name']} - {row['course_name']} \n"

                message += row

                print('no submission time, and just updated')
            else:
                print("already upload submission time")
                pass

        except:
            row = f"{row['student_name']}-{row['assignment_name']} - {row['course_name']} \n"

            error += f'{row}\n'

            print("Something wrong, please check")

            pass

    # print(row['submission_time'])

    if len(message) > 0:
        slack_bot('GS Late Script - Success run')
    #     slack_bot(message, 'msg')

    if len(error) > 0:
        slack_bot('***************************** Errors **************************')
        slack_bot(error)
        log_error_message(msg=error)
        error += f'{error}\n'
        # slack_bot(error, 'msg')

        # send_emails(error)

    # if len(message) > 0:
    #     slack_bot('************************** Download File *********************', 'msg')
    #     slack_bot(None, 'file')

    # if len(message) == 0 and len(error) == 0:
    #     slack_bot('No late submissions', 'msg')


if __name__ == '__main__':
    canvas = Canvas()
    canvas.instance = 'LPS_Production'

    gradescope.run_files()

    time.sleep(5)

    access_files()

    # send_emails('hello')

    # check_student_enrollment(82011061, 1657476)
    # check_submission_time(1831683, 12992192, 89457254)
    #
    # check_submission_time(1694819, 10711034, 14605064)

    # upload_submission_time(1694798, 10710421, 80601151, '2023-02-04 05:17:32')
    # get_student_id(90310864)
    # course_id, assignment_id, user_id, submission_time
    # upload_submission_time(1711612, 11146165, 84091923, '2023-06-01 16:41:24')
