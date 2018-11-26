# sns-lambda-slack
Alarm messages from AWS Cloud Watch to slack chat.

Environment variables:

1) SLACK_CHANNEL - paste name of the channel or ID.
2) SLACK_WEBHOOK - paste slack webhook.

Launch:
1) Create a topic.
2) Make a subsriber with lambda function.
3) Create Cloud Watch Alarm with specific infrom topic.
