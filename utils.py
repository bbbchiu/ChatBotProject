import requests
import os

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN") 


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_image_url(id, img_url):
    pass

def send_add_button_message(id):
    print("In send button")
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient":{"id": id},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Please Choose Category:",
                    "buttons": [
                        {
                            "type":"postback",
                            "title":"Food",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        },
                        {
                            "type":"postback",
                            "title":"Daily_Necessity",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        },
                        {
                            "type":"postback",
                            "title":"Others",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            }
        }
    }
    print("send button")
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
        
