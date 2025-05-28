import requests
import json
from datetime import timedelta, datetime
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from Slack_bot.slack_bot import slack_bot
from Slack_bot import updated_slack_bot
import time



matplotlib.style.use('fivethirtyeight')

current_day = date.today()
filt_week = (current_day - timedelta(days=7)).strftime('%Y-%m-%dT00:00:00-04:00')
data_title = (current_day - timedelta(days=7)).strftime('%m-%d')

url = "https://api.waitwhile.com/v2/analytics/visits"

headers = {
    "accept": "application/json",
    "apikey": ""
}

parameters = {
    'fromDate': f'{filt_week}',
    'toDate':f'{current_day}T00:00:00-04:00',

}


r = requests.get(url, params=parameters, headers=headers).json()['locations']

data = {"name":[],"numWaitlisted":[],"numServed":[],"numUniqueCustomers":[],"numCancelled":[],"numBookingsMade":[]}
# data = {"name":[],"numServed":[]}


for course in r:
  # print(course["name"])
  # print(course["numVisits"])
  # print(course["numWaitlisted"])
  # print(course["numCancelled"])
  # print(course["numBookingsMade"])
  # print(course["numServed"])
  # print(course["numUniqueCustomers"])

  data["name"].append(course["name"])
  data["numWaitlisted"].append(course["numWaitlisted"])
  data["numCancelled"].append(course["numCancelled"])
  data["numBookingsMade"].append(course["numBookingsMade"])
  data["numServed"].append(course["numServed"])
  data["numUniqueCustomers"].append(course["numUniqueCustomers"])

def format_course_tile(df):
  df = df.rsplit(" ")[-1]
  return df

keys = ['5910', '5920', '5930','5940','5950','5960','5210','5450','5500','5150','5240','5530','5410','5420','5740','5490','5300','5830','5470','5690','5160']

df = pd.DataFrame.from_dict(data)

df["name"] = df["name"].apply(format_course_tile)

df = df.set_index('name')
df.index.name = None
df = df.reindex(keys)

print(df)


ax = df.plot.bar(fontsize=9, figsize=(12, 9), rot=0)

for patch in ax.patches:
    ax.text(
        patch.get_x(),
        patch.get_height() + 1,
        " {:,}".format(int(patch.get_height())),
        fontsize=10,
        color='dimgrey',

    )

plt.title(f"WaitWhile Report-Week of {data_title}")

# plt.title(f"WaitWhile Report-1/15/2024 - 4/18/2024")

plt.tight_layout()

plt.xlabel("Courses")



plt.savefig(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/WaitWhile/files/TA_OHs.png')

path = '/Users/edwardt/PycharmProjects/Upenn_Piazza/WaitWhile/files/TA_OHs.png'

time.sleep(1)
# plt.show()
updated_slack_bot.upload_files(path,"C01SZS452PJ",updated_slack_bot.headers)
