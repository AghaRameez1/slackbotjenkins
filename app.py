import json

import requests
import slack
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response,jsonify, make_response
from slackeventsapi import SlackEventAdapter
import os
messages_to_send = {
    'workflowForm': {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "My App",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "block_id": "workflow_id",
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "Branch: main",
                            "emoji": True
                        },
                        "value": "main"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Branch: main",
                                "emoji": True
                            },
                            "value": "main"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Use workflow from",
                    "emoji": True
                }
            },
            {
                "block_id": "customer_id",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Customer short name *",
                    "emoji": True
                }
            },
            {
                "block_id": "environment_id",
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "Lower",
                            "emoji": True
                        },
                        "value": "Lower"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Lower",
                                "emoji": True
                            },
                            "value": "Lower"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Upper",
                                "emoji": True
                            },
                            "value": "Upper"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Environment name (Lower/Upper)",
                    "emoji": True
                }
            },
            {
                "block_id": "customertype_id",
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "customer",
                            "emoji": True
                        },
                        "value": "customer"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "customer",
                                "emoji": True
                            },
                            "value": "customer"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "sre-tools",
                                "emoji": True
                            },
                            "value": "sre-tools"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "The type of the customer (customer/sre-tools)",
                    "emoji": True
                }
            },
            {
                "block_id": "pipeline_id",
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "skip",
                            "emoji": True
                        },
                        "value": "skip"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "skip",
                                "emoji": True
                            },
                            "value": "skip"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "run",
                                "emoji": True
                            },
                            "value": "run"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "dns pipeline run or skip * ",
                    "emoji": True
                }
            }
        ]
    }
}
workflowTemplate = {
    "color": "{0}",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{0} GitHub Actions\n"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*repo:*\n<{0}|{1}>"
                },
                {
                    "type": "mrkdwn",
                    "text": "*message:*\n<{0}/commit/{1}|{2}>"
                },
                {
                    "type": "mrkdwn",
                    "text": "*action:*\n<{0}/commit/{1}/checks| action>"
                },
                {
                    "type": "mrkdwn",
                    "text": "*author:*\n{0} {1}"
                }
            ]
        }
    ]
}
# This is slack token
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SIGNING_SECRET = os.environ['SIGNING_SECRET']
ACCESS_TOKEN = ''
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slacks/events', app)
client = slack.WebClient(token=SLACK_TOKEN)
sched = BackgroundScheduler(daemon=True)


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if text == "hi":
        try:
            client.views_open(channel=channel_id, **messages_to_send['workflowForm'])

        except:
            print('no hi found')


@app.route('/pipelinesubmit', methods=['POST', 'GET'])
def actions():
    block_ids = []
    responses = []
    data = json.loads(request.form.get('payload', {}))
    views_data = data['view']
    for i in views_data['blocks']:
        block_ids.append(i['block_id'])
    state_value = views_data['state']['values']
    try:
        for i in block_ids:
            if i in state_value:
                if 'static_select-action' in state_value[i]:
                    responses.append(state_value[i]['static_select-action']['selected_option']['value'])
                elif 'plain_text_input-action' in state_value[i]:
                    responses.append(state_value[i]['plain_text_input-action']['value'])
        dicttoSend = json.dumps({'text': 'Your pipeline will be starting soon'})

        acknowledgewithMessage(dicttoSend)
        datatoSend = json.dumps({
            "ref": responses[0],
            "inputs": {
                "target_env": responses[2],
                "customer_type": responses[3],
                "dns_pipeline": responses[4],
                "customer_name": responses[1]
            }
        })
        runpipeline(datatoSend)
        sched.add_job(checkStatusofpipeline, 'interval', seconds=5, id='pipelineCheck')
        sched.start()
        return Response(), 200

    except Exception as e:
        print(e)


def acknowledgewithMessage(data):
    headers = {'Content-type': 'application/json'}
    requests.post('https://hooks.slack.com/services/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',
                  data=data, headers=headers)


def runpipeline(data):
    headers2 = {'Accpet': 'application/vnd.github.everest-preview+json', 'Content-type': 'application/json',
                'Authorization': 'token '+os.environ['GITHUB_TOKEN']}
    res1 = requests.post(
        'https://api.github.com/repos/hasnaineurus/hasnain-identityproider/actions/workflows/github.yml/dispatches',
        data=data, headers=headers2)
    print('response from server:', res1)


@app.route('/pipeline1', methods=['POST'])
def runpipelineModal():
    trigger_id = request.form.get('trigger_id', {})
    # channel_id = request.form.get('channel_id', {})
    client.views_open(trigger_id=trigger_id, view=messages_to_send['workflowForm'])
    return Response(), 200


def checkStatusofpipeline():
    try:
        headers2 = {'Accpet': 'application/vnd.github.everest-preview+json', 'Content-type': 'application/json',
                    'Authorization': 'token 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 '}
        res1 = requests.get('https://api.github.com/repos/hasnaineurus/hasnain-identityproider/actions/runs',
                            headers=headers2)
        data = json.loads(res1.text)
        html_url = data['workflow_runs'][0]['repository']['html_url']
        repo_full_name = data['workflow_runs'][0]['repository']['full_name']
        author_name = data['workflow_runs'][0]['head_commit']['author']['name']
        author_email = data['workflow_runs'][0]['head_commit']['author']['email']
        commit_message = data['workflow_runs'][0]['head_commit']['message']
        head_sha = data['workflow_runs'][0]['head_sha']
        status = data['workflow_runs'][0]['status']
        conclusion = data['workflow_runs'][0].get('conclusion', None)
        headers = {'Content-type': 'application/json'}
        workflow_data = [workflowTemplate]
        workflow_data[0]['blocks'][1]['fields'][0]['text'] = \
            workflow_data[0]['blocks'][1]['fields'][0]['text'].format(html_url, repo_full_name)
        workflow_data[0]['blocks'][1]['fields'][1]['text'] = \
            workflow_data[0]['blocks'][1]['fields'][1]['text'].format(html_url, head_sha,
                                                                      commit_message)
        workflow_data[0]['blocks'][1]['fields'][2]['text'] = \
            workflow_data[0]['blocks'][1]['fields'][2]['text'].format(html_url, head_sha)
        workflow_data[0]['blocks'][1]['fields'][3]['text'] = \
            workflow_data[0]['blocks'][1]['fields'][3]['text'].format(author_name, author_email)

        if status == 'completed' and conclusion == 'success':
            workflow_data[0]['color'] = workflow_data[0]['color'].format('2eb886')
            workflow_data[0]['blocks'][0]['text']['text'] = workflow_data[0]['blocks'][0]['text']['text'].format(
                '✅ Succeeded')
            dicttoSend = json.dumps({'attachments': workflow_data})
            res3 = requests.post('https://hooks.slack.com/services/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',
                                 data=dicttoSend, headers=headers)
            # # Shut down the scheduler when exiting the app
            sched.remove_job('pipelineCheck')
            workflow_data[0]['color'] = "{0}"
            workflow_data[0]['blocks'][0]['text']['text'] = "{0} GitHub Actions\n"
        elif status == 'completed' and conclusion == 'failure':
            workflow_data[0]['color'] = workflow_data[0]['color'].format('#FF0000')
            workflow_data[0]['blocks'][0]['text']['text'] = workflow_data[0]['blocks'][0]['text']['text'].format(
                '🚨 Failed')
            dicttoSend = json.dumps({'attachments': workflow_data})
            res3 = requests.post('https://hooks.slack.com/services/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',
                                 data=dicttoSend, headers=headers)
            # # Shut down the scheduler when exiting the app
            sched.remove_job('pipelineCheck')
            workflow_data[0]['color'] = "{0}"
            workflow_data[0]['blocks'][0]['text']['text'] = "{0} GitHub Actions\n"
        elif status == 'queued' and conclusion is None:
            workflow_data[0]['color'] = workflow_data[0]['color'].format('#E6792C')
            workflow_data[0]['blocks'][0]['text']['text'] = workflow_data[0]['blocks'][0]['text']['text'].format(
                '🚶🚶🚶🚶 In Queue')
            dicttoSend = json.dumps({'attachments': workflow_data})
            res3 = requests.post('https://hooks.slack.com/services/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',
                                 data=dicttoSend, headers=headers)
            workflow_data[0]['color'] = "{0}"
            workflow_data[0]['blocks'][0]['text']['text']="{0} GitHub Actions\n"
        elif status == 'in_progress' and conclusion is None:
            workflow_data[0]['color'] = workflow_data[0]['color'].format('#0000D1')
            workflow_data[0]['blocks'][0]['text']['text'] = workflow_data[0]['blocks'][0]['text']['text'].format(
                '🚧 In Progress')
            dicttoSend = json.dumps({'attachments': workflow_data})
            res3 = requests.post('https://hooks.slack.com/services/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',
                                 data=dicttoSend, headers=headers)
            workflow_data[0]['color'] = "{0}"
            workflow_data[0]['blocks'][0]['text']['text'] = "{0} GitHub Actions\n"
    except Exception as e:
        print(e)


@app.route('/docker', methods=['GET'])
def docker():
    print(os.environ)
    return make_response(jsonify(os.environ['GITHUB_TOKEN'],os.environ['SLACK_TOKEN'],os.environ['SIGNING_SECRET']),200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
