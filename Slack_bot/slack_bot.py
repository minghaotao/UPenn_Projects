import json
from slacker import Slacker

def load_json():
    with open("/Users/edwardt/PycharmProjects/Upenn_Piazza/ed_discussion/main/cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message,channel_id,file_path):
    cred = load_json()
    bot = Slacker(cred["slack_token_staff"])
    channel = channel_id
    bot_name = "ed_bot"

    # bot.chat.post_message(channel, as_user=bot_name,
    #                       text=f"{message}")
    bot.files.upload(channels=channel,
                  file_=f"{file_path}/{message}.png")



if __name__ == '__main__':
    pass