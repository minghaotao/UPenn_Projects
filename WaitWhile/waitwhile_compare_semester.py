import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('fivethirtyeight')

df = pd.read_csv('waitwhile_.csv')
df.columns = df.columns.str.strip()

# Sort the data by 'course'
df = df.sort_values(by='course',ascending=False)
# print(df)

custom_order = ['5910', '5920', '5930', '5940', '5950', '5960', '5500', '5450', '5420', '5410', '5210', '5510', '5530',
                '5740', '5830', '5850', '5980', '5490', '5460', '5810']

# ['5210', '5510', '5530', '5740', '5830', '5850' , '5980', '5490', '5460', '5810']
grouped_data = df.pivot(index='course', columns='Semester', values='Average Sessions per student')
grouped_data = grouped_data.fillna(0)
print(grouped_data)
grouped_data = grouped_data.sort_values(by='Fall 2024',ascending=False)
print(grouped_data)

ax = grouped_data.plot(kind='bar', figsize=(12, 8))

for patch in ax.patches:
    ax.text(
        patch.get_x(),
        patch.get_height(),
        f"{patch.get_height():.2f}",
        fontsize=10,
        color='dimgrey',

    )

# Add labels and title
plt.title('Average number of times each student attedned a TA session')
plt.xlabel('Course')
plt.ylabel('Average Sessions per student')
plt.legend(title='Semester')


plt.savefig(f'/Users/edwardt/PycharmProjects/Upenn_Piazza/WaitWhile/files/TA_OHs_Semesters_Average.png')
plt.show()