import threading
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from decouple import config

class SlackBot:
    def __init__(self):
        self.client = WebClient(token=config("SLACK_BOT_TOKEN"))

    def get_channel_id(self, channel_name):
        try:
            result = self.client.conversations_list(types=['private_channel', 'public_channel'])
            channels = result['channels']
            for channel in channels:
                if channel['name'] == channel_name:
                    return channel['id']
            print("No id Found")
            return None
        except SlackApiError as e:
            print(f"Error retrieving channels: {e.response['error']}")
            return None
    def get_user_by_email(self, email):
        from .helper import users
        try:
            # Retrieve all users
            # result = self.client.users_list()
            # users = result['members']
            # print("users", users[2]['profile'].get("email"))
            
            for user in users:
                if user['profile'].get('email') == email:
                    return user['id']
            print(f"User '{email}' not found.")
            return None
        except SlackApiError as e:
            print(f"Error retrieving users: {e.response['error']}")
            return None

    def get_user_by_username(self, username):
        from .helper import users
        try:
            # Retrieve all users
            # result = self.client.users_list()
            # users = result['members']
            # print("users", users[2]['profile'].get("email"))
            
            for user in users:
                if username and user['name'] == username:
                    return user['id']
            print(f"User '{username}' not found.")
            return None
        except SlackApiError as e:
            print(f"Error retrieving users: {e.response['error']}")
            return None

    def send_message_to_user(self, user_id, text):
        def send_message():
            try:
                response = self.client.chat_postMessage(
                    channel=user_id,
                    text=text,
                )
            except SlackApiError as e:
                print(f"Error sending message to user: {e.response['error']}")

        threading.Thread(target=send_message).start()

    def send_message_to_channel(self, channel_id, text):
        def send_message():
            try:
                response = self.client.chat_postMessage(
                    channel=channel_id,
                    text=text
                )
                print(f"Message sent successfully {response}")
            except SlackApiError as e:
                print(f"Error sending message to channel: {e.response['error']}")

        threading.Thread(target=send_message).start()

    def send_message_to_all_participants(self, channel_id, text):
        def send_messages():
            try:
                # Retrieve the list of users in the channel
                response = self.client.conversations_members(channel=channel_id)
                users = response['members']
                for user_id in users:
                    self.send_message_to_user(user_id, text)
            except SlackApiError as e:
                print(f"Error sending message to all participants: {e.response['error']}")

        threading.Thread(target=send_messages).start()
