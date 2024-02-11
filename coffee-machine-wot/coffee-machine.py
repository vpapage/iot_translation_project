#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is an example of Web of Things producer ("server" mode) Thing script.
It considers a fictional smart coffee machine in order to demonstrate the capabilities of Web of Things.
The example is ported from the node-wot environment -
https://github.com/eclipse/thingweb.node-wot/blob/master/packages/examples/src/scripts/coffee-machine.ts.
'''
import asyncio
import json
import logging
import math

from wotpy.protocols.http.server import HTTPServer
from wotpy.protocols.ws.server import WebsocketServer
from wotpy.wot.servient import Servient

CATALOGUE_PORT = 9090
WEBSOCKET_PORT = 9393
HTTP_PORT = 9494

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

TD = {
    'title': 'Smart-Coffee-Machine',
    'id': 'urn:dev:wot:coffee-machine:101',
    'description': '''A smart coffee machine with a range of capabilities.
A complementary tutorial is available at http://www.thingweb.io/smart-coffee-machine.html.''',
    'support': 'git://github.com/eclipse/thingweb.node-wot.git',
    '@context': [
        'https://www.w3.org/2019/wot/td/v1',
    ],
    'securityDefinitions': {
        'nosec_sc':{
            'scheme':'nosec' 
        }
    },
    'security': 'nosec_sc',
    'properties': {
        'possibleDrinks': {
            'type': 'array',
            'description': '''The list of possible drinks in general. Doesn't depend on the available resources.''',
            'items': {
                'type': 'string',
            }
        },
        'maintenanceNeeded': {
            'type': 'boolean',
            'description': '''Shows whether a maintenance is needed. The property is observable. Automatically set to True when the servedCounter property exceeds 1000.''',
            'observable': True,
            },
        },
    'actions': {
        'makeDrink': {
            'description': '''Make a drink from available list of beverages. Accepts drink id as input.''',
            'input': {
                'type': 'string',
                'description': '''Defines what drink to make, one of possibleDrinks property values, e.g. latte.''',
            },
            'output': {
                'type': 'string',
                'description': '''Returns a message when all invoked promises are resolved (asynchronous).''',
            },
        },
    },
    'events': {
        'maintenanceAlert': {    
            'description': '''Maintenance alert. Emitted when the maintenanceNeeded property is true.''',
            'data': {
                'type': 'string',
            },
        },
    },
}


async def main():
    LOGGER.info('Creating WebSocket server on: {}'.format(WEBSOCKET_PORT))
    ws_server = WebsocketServer(port=WEBSOCKET_PORT)

    LOGGER.info('Creating HTTP server on: {}'.format(HTTP_PORT))
    http_server = HTTPServer(port=HTTP_PORT)

    LOGGER.info('Creating servient with TD catalogue on: {}'.format(CATALOGUE_PORT))
    servient = Servient(catalogue_port=CATALOGUE_PORT)
    servient.add_server(ws_server)
    servient.add_server(http_server)

    LOGGER.info('Starting servient')
    wot = await servient.start()

    LOGGER.info('Exposing and configuring Thing')

    # Produce the Thing from Thing Description
    exposed_thing = wot.produce(json.dumps(TD))

    # Initialize the property values
    await exposed_thing.properties['possibleDrinks'].write(['espresso', 'americano', 'cappuccino', 'latte', 'hotChocolate', 'hotWater'])
    await exposed_thing.properties['maintenanceNeeded'].write(False)
    
    # Observe the value of maintenanceNeeded property
    exposed_thing.properties['maintenanceNeeded'].subscribe(

        # Notify a "maintainer" when the value has changed
        # (the notify function here simply logs a message to the console)

        on_next=lambda data: notify(f'Value changed for an observable property: {data}'),
        on_completed=notify('Subscribed for an observable property: maintenanceNeeded'),
        on_error=lambda error: notify(f'Error for an observable property maintenanceNeeded: {error}')
    )
    
    # Set up a handler for makeDrink action
    async def make_drink_action_handler(params):
        
        # Check if params are provided, else give default value
        drinkId = 'espresso'
        drinkId = params.get('input', drinkId)
        
        # Deliver the drink
        return f'Your {drinkId} is in progress!'

    exposed_thing.set_action_handler('makeDrink', make_drink_action_handler)

    exposed_thing.expose()
    LOGGER.info(f'{TD["title"]} is ready')


def read_from_sensor(sensorType):
    # Actual implementation of reading data from a sensor can go here
    # For the sake of example, let's just return a value
    return 100


def notify(msg, subscribers=['admin@coffeeMachine.com']):
    # Actual implementation of notifying subscribers with a message can go here
    LOGGER.info(msg)


if __name__ == '__main__':
    LOGGER.info('Starting loop')
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
