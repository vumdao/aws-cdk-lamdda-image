#!/usr/bin/env python
from datetime import datetime
import json
import requests


def handler(event, context):
    webhook_url = 'https://hooks.slack.com/services/WORKSPACE_ID/WEBHOOK_ID'
    footer_icon = 'https://static.io/img/cdk.png'
    color = '#36C5F0'
    level = ':white_check_mark: INFO :white_check_mark:'
    curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = event['msg']
    slack_payload = {"username": "Docker-Image",
                     "attachments": [{"fallback": "Required plain-text summary of the attachment.",
                                      "pretext": level,
                                      "color": color,
                                      "text": message,
                                      "footer": curr_time,
                                      "footer_icon": footer_icon}]}
    requests.post(webhook_url, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
