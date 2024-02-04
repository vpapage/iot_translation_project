#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is an example of Web of Things consumer ("client" mode) Thing script.
It considers a fictional smart coffee machine in order to demonstrate the capabilities of Web of Things.
The example is ported from the node-wot environment -
https://github.com/eclipse/thingweb.node-wot/blob/master/packages/examples/src/scripts/coffee-machine-client.ts.
'''
import json
import asyncio
import logging

from wotpy.wot.servient import Servient
from wotpy.wot.wot import WoT

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


async def main():
    wot = WoT(servient=Servient())
    consumed_thing = await wot.consume_from_url('http://127.0.0.1:9090/smart-coffee-machine')

    LOGGER.info('Consumed Thing: {}'.format(consumed_thing))

    # It's also possible to set a client-side handler for observable properties
    consumed_thing.properties['maintenanceNeeded'].subscribe(
        on_next=lambda data: LOGGER.info(f'Value changed for an observable property: {data}'),
        on_completed=LOGGER.info('Subscribed for an observable property: maintenanceNeeded'),
        on_error=lambda error: LOGGER.info(f'Error for an observable property maintenanceNeeded: {error}')
    )
    
    # Now let's make 3 cups of latte!
    makeCoffee = await consumed_thing.invoke_action('makeDrink', {'drinkId': 'latte'})
    LOGGER.info(makeCoffee)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
