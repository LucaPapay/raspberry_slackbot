from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import bot_token, app_token, google_mail, google_password
from selenium_driver import SeleniumDriver


def start_app():
    # Install the Slack app and get xoxb- token in advance
    app = App(token=bot_token)
    selenium_driver = SeleniumDriver()

    @app.command("/link")
    def handle_link_command(ack, body, logger):
        logger.info(body)
        user_id = body["user_id"]
        text = body["text"]
        link = get_first_url_in_string(text)
        if link:
            ack(f"Hi <@{user_id}>! I found a link: {link}!")
            selenium_driver.open_url(link)

        else:
            ack(f"Hi <@{user_id}>! I couldn't find a link in your message.")

    @app.command("/share-screen")
    def handle_start_meeting_command(ack, body, logger):
        logger.info(body)
        user_id = body["user_id"]
        ack(f"Hi <@{user_id}>! I'm setting up a meeting for you.")
        selenium_driver.google_login(google_mail, google_password)
        meeting_url = selenium_driver.start_meeting()
        app.client.chat_postMessage(channel=body["channel_id"], text=f"Hi <@{user_id}>! Here's your meeting link: {meeting_url}")

    SocketModeHandler(app, app_token).start()


def get_first_url_in_string(text):
    found = ""
    for word in text.split():
        if word.startswith("http") or word.startswith("www"):
            found = word
            break
    return found


if __name__ == "__main__":
    start_app()
