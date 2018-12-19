from bottle import route, run, request, abort, static_file
import os
from fsm import TocMachine


VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
machine = TocMachine(
    states=[
        'user',
        'ready',
        'add',
        'list',
        'counting',
        'database',
        'spend'
    ],
    transitions=[
        {
            'trigger': 'wake',
            'source': 'user',
            'dest': 'ready',
            'conditions': 'is_going_to_ready'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'add',
            'conditions': 'is_going_to_add'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'list',
            'conditions': 'is_going_to_list'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'counting',
            'conditions': 'is_going_to_counting'
        },
        {
            'trigger': 'advance',
            'source': 'ready',
            'dest': 'user',
            'conditions': 'is_back_to_user'
        },
        {
            'trigger': 'addItem',
            'source': 'add',
            'dest': 'database',
            'conditions': 'is_going_to_db'
        },
        {
            'trigger': 'inFile',
            'source': 'database',
            'dest': 'spend',
            'conditions': 'is_going_to_spend'
        },
        {
            'trigger': 'go_ready',
            'source': [
                'add',
                'list',
                'counting',
                'spend'
            ],
            'dest': 'ready',
            'conditions': 'is_back_to_ready'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if machine.state == 'user':
            machine.wake(event)
            return 'OK'
        elif machine.state == 'ready':
            machine.advance(event)
            return 'OK'
        elif machine.state == 'add':
            if machine.addItem(event):
                return 'OK'
            elif machine.go_ready(event):
                return 'OK'
            else:
                pass
        elif machine.state == 'list':
            machine.go_ready(event)
            return 'OK'
        
        elif machine.state == 'counting':
            machine.go_ready(event)
            return 'OK'

        elif machine.state == 'database':
            print("In dd")
            machine.inFile(event)
            return 'OK'
        elif machine.state == 'spend':
            machine.go_ready(event)
            return 'OK'

@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
