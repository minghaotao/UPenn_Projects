import requests
import json
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import csv
from slacker import Slacker
from Slack_bot import updated_slack_bot
import os
import ed_reports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

headers = CaseInsensitiveDict()

courses = {

    '5910': 'https://us.edstem.org/api/courses/69765/analytics/discussion_threads.json',
    '5920': 'https://us.edstem.org/api/courses/69766/analytics/discussion_threads.json',


}


def load_json():
    with open("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/main/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message):
    cred = load_json()["new_slack_bot_token"]
    CHANNEL_ID = "C01SZS452PJ"
    headers = {"Authorization": f"Bearer {cred}", "Content-Type": "application/json"}
    file_path = f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/{message}.png'

    updated_slack_bot.upload_files(file_path, CHANNEL_ID, headers)
    # pass


def download_file(course, course_url):
    # headers["content-type"] = "application/x-www-form-urlencoded"
    headers = {'Authorization': 'Bearer ' + ''}
    
    r = requests.post(course_url, headers=headers)
    if r.status_code == 200:
        print(course)
        f_read = json.loads(r.text)

        ed_reports.clear_file(course)
        ed_reports.generate_file(f_read, course)
        data = ed_reports.read_file(course)
        ed_reports.write_file(data, 'reports')


def charts():
    matplotlib.style.use('fivethirtyeight')

    df = pd.read_csv("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/reports.csv")

    ax = df.plot.bar(x="Courses", y=["Total_Threads", "Total_Questions", "Current_Unresolved", "late_24Hours"],
                     fontsize=9, figsize=(10, 7), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 1,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey',

        )

    plt.title(f"Ed Discussion Report-Week of {ed_reports.filt_week}")

    plt.tight_layout()

    plt.xlabel("Courses")

    plt.savefig('/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/ed_report.png')

    ax1 = df.sort_values('Response_Rate%').plot.barh(x="Courses", y="Response_Rate%", fontsize=9, figsize=(10, 7))

    for patch in ax1.patches:
        ax1.text(
            patch.get_width(),
            patch.get_y(),
            " {:,}%".format(patch.get_width()),
            fontsize=10,
            color='dimgrey'
        )

    plt.title(f'late_24Hours_Response_Rate-Week of {ed_reports.filt_week}')

    plt.tight_layout()
    plt.savefig(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/course_files/response_rate.png')
    # plt.show()


if __name__ == '__main__':
    ed_reports.reset_file("reports")
    header = ["Courses", "Total_Threads", "Total_Questions", "Current_Unresolved", "late_24Hours", "Response_Rate%"]
    ed_reports.write_file(header, 'reports')
    for key, value in courses.items():
        download_file(key, value)

    charts()

    # download_file('5910','https://us.edstem.org/api/courses/69765/analytics/discussion_threads.json')

    # slack_bot('ed_report')
    # slack_bot('response_rate')
