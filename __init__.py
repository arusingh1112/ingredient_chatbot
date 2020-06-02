# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from mindmeld import Application

app = Application(__name__)

__all__ = ['app']


@app.handle(intent='greet')
def welcome(request, responder):
    responder.reply(
        "Hello! I can help you find out what ingredients you need for different snacks. What snack are you looking to make?")
    responder.listen()


#@app.handle(intent='list_ingredients', has_entity='snack_name')
#@app.dialogue_flow(domain='snack_ingredients', intent='list_ingredients')


@app.handle(intent='list_ingredients')
def list_ingredients(request, responder):
    active_snack = None
    snack_entity = next((e for e in request.entities if e['type'] == 'snack_name'), None)
    print(snack_entity)
    if snack_entity and snack_entity['value']:
        snacks = app.question_answerer.get(index='snacks', id=snack_entity['value'][0]['id'])
        active_snack = snacks[0]

        responder.slots['snack_name'] = active_snack['snack_name']
        responder.slots['snack_ingredients'] = active_snack['snack_ingredients']
        responder.reply("In order to make {snack_name}, you will need {snack_ingredients}.")
        return
    else:
         responder.reply(
             "Sorry, I do not know the ingredients for that snack. Is there any other snack you want to know the ingredients for?")
         responder.listen()


@app.handle(default=True)
def default(request, responder):
    responder.reply("Sorry, I do not think I can help you with that. I can help you find the list of ingredients you need to make a snack")
    responder.listen()

@app.handle(intent='exit')
def goodbye(request, responder):
    responder.reply("Enjoy! Have a nice day.")

