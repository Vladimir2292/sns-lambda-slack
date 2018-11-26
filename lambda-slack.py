import os, boto3, json
import urllib.request, urllib.parse
import logging


def cloudwatch_message(message):

    return {
            "color": "#a63657",
            "fallback": "Alarm {} triggered".format(message['AlarmName']),
            "fields": [
                { "title": "Alarm Name", "value": message['AlarmName'], "short": True },
                { "title": "Alarm Description", "value": message['AlarmDescription'], "short": False},
                { "title": "Alarm Reason", "value": message['NewStateReason'], "short": False},
                { "title": "Old State", "value": message['OldStateValue'], "short": True },
                { "title": "Current State", "value": message['NewStateValue'], "short": True }
            ]
        }


def default_message(message):
    return {
            "fallback": "A new message",
            "fields": [{"title": "Message", "value": json.dumps(message), "short": False}]
        }



def notify_slack(message):
    
    slack_url = os.environ['SLACK_WEBHOOK']
    slack_channel = os.environ['SLACK_CHANNEL']
    
    slack_emoji = ':tophat:'
    slack_username = 'Monitor Message'
    
    inform = {
        "channel": slack_channel,
        "icon_emoji": slack_emoji,
        "username": slack_username,
        "attachments": []
    }
    
    if "AlarmName" in message:
        notification = cloudwatch_message(message)
        inform['text'] = "AWS CloudWatch notification - " + message["AlarmName"]
        inform['attachments'].append(notification)
    else:
        inform['text'] = "AWS notification"
        inform['attachments'].append(default_message(message))

    inf = urllib.parse.urlencode({"payload": json.dumps(inform)}).encode("utf-8")
    req = urllib.request.Request(slack_url)
    urllib.request.urlopen(req, inf)


def lambda_handler(event, context):

    sns = event['Records'][0]['Sns']
    #load = json.dumps(sns['Message'])
    message = json.loads(sns['Message'])

    notify_slack(message)
