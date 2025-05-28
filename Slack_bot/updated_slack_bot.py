import requests
import os
import time

# Your Slack Bot Token
SLACK_BOT_TOKEN = ""
CHANNEL_ID = ""  # Replace with your actual Slack channel ID
headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
file_path = "/Users/edwardt/PycharmProjects/Upenn_Piazza/Slack_bot/test1.png"  # Replace with the actual file path


def post_message(message,CHANNEL_ID,headers):
    url = "https://slack.com/api/chat.postMessage"
    data = {"channel": CHANNEL_ID, "text": message}

    response = requests.post(url, headers=headers, json=data)
    print(response.json())


def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)  # Returns the size of the file in bytes
        return file_size
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# Step 1: Get Upload URL
def get_upload_url(file_path,headers):
    file_size = get_file_size(file_path)

    print(f"File size: {file_size} bytes")
    file_name = os.path.basename(file_path)

    # if file_size:
    url = "https://slack.com/api/files.getUploadURLExternal"
    data = {"filename": file_name, "length": file_size}

    response = requests.get(url, headers=headers, params=data)
    response_data = response.json()

    if response_data.get("ok"):
        print(response_data["upload_url"], response_data["file_id"])
        return response_data["upload_url"], response_data["file_id"]
    else:
        raise Exception(f"Error getting upload URL: {response_data}")


# Step 2: Upload File
def upload_file(upload_url, file_path):
    with open(file_path, "rb") as file:
        # headers = {"Content-Type": "image/png"}  # Adjust content type if needed
        # response = requests.put(upload_url, data=file, headers=headers)
        response = requests.post(upload_url, files={'file': file})
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            raise Exception(f"Error uploading file: {response.text}")


# Step 3: Complete Upload
def complete_upload(file_id, channel_id,headers):
    url = "https://slack.com/api/files.completeUploadExternal"
    data = {"files": [{"id": file_id}], "channel_id": channel_id}

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if response_data.get("ok"):
        print("File upload completed and shared successfully.")
        # print(response_data["files"])
        return response_data["files"]
    else:
        raise Exception(f"Error completing upload: {response_data}")


def upload_files(file_path,CHANNEL_ID,headers):
    # Run the Upload Process
    try:
        # file_size = len(open(file_path, "rb").read())
        # print(file_size)# Get file size in bytes

        upload_url, file_id = get_upload_url(file_path,headers)
        time.sleep(1)
        upload_file(upload_url, file_path)
        time.sleep(1)
        complete_upload(file_id, CHANNEL_ID,headers)
    except Exception as e:
        print(e)


# post_message("This is a test")

# upload_files(file_path,headers)

# complete_upload('F08LAQVDB96', CHANNEL_ID)
if __name__ == "__main__":
    # post_message("This is a test")
    pass
