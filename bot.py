
#Prvo doradi:
#pip install flask
#pip install viberbot

import threading
import time
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from sched import scheduler

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Veki Bot',
    avatar='',
    auth_token='TOKEN'
))

def setWebhook(bot):
    bot.set_webhook('NAS URL ZA WEBHOOK')

@app.route('/', methods=['POST'])
def incoming():
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        #Izdvaja se poruka i senderid kome odgovaramo
        msg = viber_request.message
        cId = viber_request.sender.id
        #Analizira se poruka i salej se odgovor (OVDE STAVLAJMO VIBER ENDPOINTE)
        if msg=="Hello World":
            viber.send_message(cId, [
                TextMessage(text="Hello World!")
            ])

    return Response(status=200)

if __name__ == "__main__":
    #Webhook ide na poseban thread
    s = scheduler(time.time, time.sleep)
    s.enter(5,1,setWebhook,(viber))
    t=threading.Thread(target=scheduler.run)
    t.start()
    #URL za server kolko sam provalio ne sme da bude isti kao URL za webhook
    app.run(host='HOST URL ZA NAS SERVER', port=8000, debug=True)