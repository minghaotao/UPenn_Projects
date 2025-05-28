import pandas as pd
import requests
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import os
from slacker import Slacker
import json
from Slack_bot import updated_slack_bot
import matplotlib

matplotlib.style.use('fivethirtyeight')

current_day = datetime.today()
filt_week = (current_day - timedelta(days=7)).strftime('%Y-%m-%d')


def load_json():
    with open("/home1/e/edtao/data_reports/extension_report/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def extension_requests():
    url = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vRWoDxDuN4vNzqjs65Bgb07Gk4DNK3otiUclU-72XgnJxGHpVrP8VlSieoA8hrahS2ncyjsYNYTVsBd/pub?output=csv'
    r = requests.get(url)
    with open('/home1/e/edtao/data_reports/extension_report/extension.csv', 'wb') as f:
        f.write(r.content)

    df = pd.read_csv("/home1/e/edtao/data_reports/extension_report/extension.csv")

    filt_week = (current_day - timedelta(days=7)).strftime('%Y-%m-%d')
    df = df.loc[df["submission_time"] >= filt_week]
    current_week = df.groupby(["Course_number"]).agg({'status': 'value_counts'})["status"].unstack().fillna(0)
    print(current_week)

    ax = current_week.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 1,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey'
        )

    plt.title(f"Assignment Extension for the week of {filt_week}")

    plt.tight_layout()

    plt.savefig('/Users/edwardt/PycharmProjects/Upenn_Piazza/Extension_pub_files/assignment-extensions.png')

    plt.show()

    print(df)


if __name__ == '__main__':
    extension_requests()
    # slack_bot()
    updated_slack_bot.upload_files('/Users/edwardt/PycharmProjects/Upenn_Piazza/Extension_pub_files/assignment-extensions.png', "C0325GADHPT", updated_slack_bot.headers)
