from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import bot_token, app_token


def start_app():
    # Install the Slack app and get xoxb- token in advance
    app = App(token=bot_token)
    @app.command("/link")
    def handle_link_command(ack, body, logger):
        user_id = body["user_id"]
        ack(f"Hi <@{user_id}>!")
        logger.info(f"link command is called by user {user_id}")


    SocketModeHandler(app, app_token).start()


if __name__ == "__main__":
    start_app()
