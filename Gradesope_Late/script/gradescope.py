import json
import requests
import pandas as pd
from io import StringIO
import numpy as np
import csv
import file_mapping
from datetime import datetime, timedelta
import sync_roster

pd.options.mode.chained_assignment = None


def download_data(course_number):
    cookies = {
        'signed_token': '',
    }

    r = requests.get(file_mapping.course_url[f'{course_number}'], cookies=cookies).text

    df = pd.read_csv(StringIO(r))

    return df


def clear_file():
    headers = ["Lateness (H:M:S)", "submission_time", "SID", "course_name", "student_name", "assignment_id",
               "assignment_name", "Canvas_course_id"]
    with open(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/late_files/late_submissions.csv',
              mode='w') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow(headers)


def late_columns(df):
    filter_late_columns = df.columns.str.contains('Lateness')

    late = df.loc[:, filter_late_columns]

    return late.columns.tolist()


def get_canvas_course_id(df):
    course_id = df["Sections"].unique().tolist()
    print(course_id)

    course_id = [i.split('-') for i in course_id]

    for key, value in file_mapping.canvas_id_map.items():

        for i in course_id[0]:
            if key in i:
                print(key, value)

                return value


def update_time_zone(df):
    current_time = datetime.strptime(df, f'%Y-%m-%d %H:%M:%S')

    update_time = (current_time + timedelta(hours=3)).strftime(f'%Y-%m-%d %H:%M:%S')

    return update_time


def get_late_submission_time(df, late_column_name, course_number):
    if len(df[late_column_name].unique()) > 1:
        new_submission_name = late_column_name.rsplit('-', 1)[0] + '- Submission Time'

        df = df[df[late_column_name].notnull()]

        df['student_name'] = df['First Name'] + ' ' + df['Last Name']

        df = df[[late_column_name, new_submission_name, 'SID', 'Sections', 'student_name']].reset_index().drop(
            columns='index')

        df[new_submission_name] = df[new_submission_name].str[:-6]

        # print(df[new_submission_name])

        df['assignment_id'] = file_mapping.assignment_map[f'{course_number}'][new_submission_name]
        print(df['assignment_id'] )

        df['assignment_name'] = late_column_name.rsplit('-', 1)[0]

        df['canvas_course_id'] = get_canvas_course_id(df)

        # df['course_name'] = course_name

        df['SID'] = df['SID'].astype(int)

        df = df.rename(columns={f"{late_column_name}": "Lateness (H:M:S)", f"{new_submission_name}": "submission_time"})

        # df['submission_time'] = df['submission_time'].apply(update_time_zone)
        #adjust the timestamp based on the time from the Gradescope 2023-10-09 21:17:29 -0400

        # print(df)
        df.to_csv('/Users/edwardt/PycharmProjects/Upenn_Piazza/GS_Late/late_files/late_submissions.csv',
                  index=False,
                  header=False, mode='a')
        print(df)


def read_data(course_number):

    df = download_data(course_number)

    print(df)

    df = df.loc[:, df.columns.isin(file_mapping.filters[f'{course_number}'])].sort_index(axis=1)

    df = df.replace('00:00:00', np.nan)

    df = df[df["Sections"].notnull()]

    late = late_columns(df)
    for row in late:
        get_late_submission_time(df, row, course_number)
        # print(row)



def run_files():
    clear_file()
    for course, data in file_mapping.course_url.items():
        read_data(course)


if __name__ == '__main__':

    run_files()
