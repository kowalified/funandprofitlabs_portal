""" sends a message to spark room """
import requests
from flask import current_app as app

def send_message_to_room(room_id, message):
    """ sends a message to spark room """
    spark_host = "https://api.ciscospark.com/"
    spark_headers = {}
    spark_headers["Content-type"] = "application/json"
    spark_headers["Authorization"] = "Bearer " + app.config["SPARK_BOT_TOKEN"]
    app_headers = {}
    app_headers["Content-type"] = "application/json"

    spark_u = spark_host + "v1/messages"
    message_body = {
        "roomId" : room_id,
        "markdown" : message
    }
    page = requests.post(spark_u, headers=spark_headers, json=message_body)
    message = page.json()
    return message
