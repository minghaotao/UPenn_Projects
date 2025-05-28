import requests
import file_mapping
import gs_main

cookies = {
    'signed_token': '',
    'remember_me': '',
    '__stripe_mid': '2a52f447-4a30-4582-892c-ca0d27c3323c29e556',
    '_gcl_au': '1.1.57906742.1664231556',
    '_fbp': 'fb.1.1664231555839.506266745',
    '_ga': 'GA1.1.1254934193.1633365732',
    '_ga_7Z1WNTTCRG': 'GS1.1.1668200691.4.0.1668200691.0.0.0',
    '__stripe_sid': '4adf2575-308a-49f0-871d-e2602d39291308fd07',
    'apt.sid': 'AP-1BQVLBSZC216-2-1669221683760-31118397',
    'apt.uid': 'AP-1BQVLBSZC216-2-1669221683760-16791356.0.2.cffb8c90-9c2f-4319-81f1-b2a3827fc501',
    '_gradescope_session': '',
}

headers = {
    'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.gradescope.com',
    'Referer': 'https://www.gradescope.com/courses/403672/memberships',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'X-CSRF-Token': 'UXYKeNnFXrvW0QicQ+rF9lQ/dB+mpwRlNhpmCC3gdGAicgpEpnqWBYtfXCuyIFhATf7rtyupx85P6PwaG/bdmA==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

data = {
    'utf8': '✓',
    'button': '',
}


def request_roster_(course):
    r = requests.post(f'https://www.gradescope.com/courses/{course}/canvas/update_roster', cookies=cookies,
                      headers=headers, data=data)

    if r.status_code == 200:

        print(r.text)

    else:
        raise Exception(r.status_code, r.text)


def sync_roster_():
    for course, data in file_mapping.course_url.items():
        data = data.rsplit('/', 2)[1]

        request_roster_(data)

    gs_main.slack_bot('GS Roster have been synced', 'msg')


if __name__ == '__main__':
    sync_roster_()
