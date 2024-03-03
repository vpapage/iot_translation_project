#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classes that contain the client logic for the HTTP protocol.
"""

import asyncio
import json
import logging
import time

import tornado.httpclient
import reactivex
from tornado.simple_httpclient import HTTPTimeoutError

from wotpy.protocols.client import BaseProtocolClient
from wotpy.protocols.enums import Protocols, InteractionVerbs
from wotpy.protocols.exceptions import FormNotFoundException, ClientRequestTimeout
from wotpy.protocols.http.enums import HTTPSchemes
from wotpy.protocols.utils import is_scheme_form
from wotpy.utils.utils import handle_observer_finalization
from wotpy.wot.events import EmittedEvent, PropertyChangeEmittedEvent, PropertyChangeEventInit
from wotpy.protocols.http.credential import BaseCredential


class HTTPClient(BaseProtocolClient):
    """Implementation of the protocol client interface for the HTTP protocol."""

    JSON_HEADERS = {"Content-Type": "application/json"}
    DEFAULT_CON_TIMEOUT = 60
    DEFAULT_REQ_TIMEOUT = 60

    def __init__(self, connect_timeout=DEFAULT_CON_TIMEOUT, request_timeout=DEFAULT_REQ_TIMEOUT):
        self._connect_timeout = connect_timeout
        self._request_timeout = request_timeout
        self._logr = logging.getLogger(__name__)
        self._credential = None
        super().__init__()

    @classmethod
    def pick_http_href(cls, td, forms, op=None):
        """Picks the most appropriate HTTP form href from the given list of forms."""

        def is_op_form(form):
            try:
                return op is None or op == form.op or op in form.op
            except TypeError:
                return False

        def find_href(scheme):
            try:
                return next(
                    form.href for form in forms
                    if is_scheme_form(form, td.base, scheme) and is_op_form(form))
            except StopIteration:
                return None

        form_https = find_href(HTTPSchemes.HTTPS)

        return form_https if form_https is not None else find_href(HTTPSchemes.HTTP)

    @property
    def protocol(self):
        """Protocol of this client instance.
        A member of the Protocols enum."""

        return Protocols.HTTP

    @property
    def connect_timeout(self):
        """Returns the default connection timeout for all HTTP requests."""

        return self._connect_timeout

    @property
    def request_timeout(self):
        """Returns the default request timeout for all HTTP requests."""

        return self._request_timeout

    def is_supported_interaction(self, td, name):
        """Returns True if the any of the Forms for the Interaction
        with the given name is supported in this Protocol Binding client."""

        forms = td.get_forms(name)

        forms_http = [
            form for form in forms
            if is_scheme_form(form, td.base, HTTPSchemes.list())
        ]

        return len(forms_http) > 0

    def set_security(self, security_scheme_dict, credentials):
        """Sets the security credentials for the given security scheme."""

        credential = BaseCredential.build(security_scheme_dict, credentials)
        self._credential = credential

    async def sign_request(self, request):
        """Adds the appropriate authorization header to the request
        and delegates the addition of the header to the credential class."""

        if self._credential:
            return await self._credential.sign(request)

        return request

    async def invoke_action(self, td, name, input_value, timeout=None):
        """Invokes an Action on a remote Thing.
        Returns a Future."""

        con_timeout = timeout if timeout else self._connect_timeout
        req_timeout = timeout if timeout else self._request_timeout

        now = time.time()

        href = self.pick_http_href(td, td.get_action_forms(name))

        if href is None:
            raise FormNotFoundException()

        body = json.dumps({"input": input_value})
        http_client = tornado.httpclient.AsyncHTTPClient()

        try:
            http_request = tornado.httpclient.HTTPRequest(
                href, method="POST",
                body=body,
                headers=self.JSON_HEADERS,
                connect_timeout=con_timeout,
                request_timeout=req_timeout,
                validate_cert=False)
        except HTTPTimeoutError:
            raise ClientRequestTimeout

        response = await http_client.fetch(await self.sign_request(http_request))
        resp_body = json.loads(response.body)

        if resp_body.get("error") is not None:
            raise Exception(resp_body.get("error"))
        else:
            return resp_body.get("result")

    async def write_property(self, td, name, value, timeout=None):
        """Updates the value of a Property on a remote Thing.
        Returns a Future."""

        con_timeout = timeout if timeout else self._connect_timeout
        req_timeout = timeout if timeout else self._request_timeout

        href = self.pick_http_href(td, td.get_property_forms(name))

        if href is None:
            raise FormNotFoundException()

        http_client = tornado.httpclient.AsyncHTTPClient()
        body = json.dumps({"value": value})

        try:
            http_request = tornado.httpclient.HTTPRequest(
                href, method="PUT", body=body,
                headers=self.JSON_HEADERS,
                connect_timeout=con_timeout,
                request_timeout=req_timeout,
                validate_cert=False)
        except HTTPTimeoutError:
            raise ClientRequestTimeout

        await http_client.fetch(http_request)

    async def read_property(self, td, name, timeout=None):
        """Reads the value of a Property on a remote Thing.
        Returns a Future."""

        con_timeout = timeout if timeout else self._connect_timeout
        req_timeout = timeout if timeout else self._request_timeout

        href = self.pick_http_href(td, td.get_property_forms(name))

        if href is None:
            raise FormNotFoundException()

        http_client = tornado.httpclient.AsyncHTTPClient()

        try:
            http_request = tornado.httpclient.HTTPRequest(
                href, method="GET",
                connect_timeout=con_timeout,
                request_timeout=req_timeout,
                validate_cert=False)
        except HTTPTimeoutError:
            raise ClientRequestTimeout

        response = await http_client.fetch(await self.sign_request(http_request))
        result = json.loads(response.body)
        result = result.get("value", result)

        return result

    def on_event(self, td, name):
        """Subscribes to an event on a remote Thing.
        Returns an Observable."""

        href = self.pick_http_href(td, td.get_event_forms(name))

        if href is None:
            raise FormNotFoundException()

        def subscribe(observer, scheduler):
            """Subscription function to observe events using the HTTP protocol."""

            state = {"active": True}

            @handle_observer_finalization(observer)
            async def callback():
                http_client = tornado.httpclient.AsyncHTTPClient()
                http_request = tornado.httpclient.HTTPRequest(href, method="GET", validate_cert=False)

                while state["active"]:
                    try:
                        response = await http_client.fetch(await self.sign_request(http_request))
                        payload = json.loads(response.body).get("payload")
                        observer.on_next(EmittedEvent(init=payload, name=name))
                    except HTTPTimeoutError:
                        pass

            def unsubscribe():
                state["active"] = False

            loop = asyncio.get_running_loop()
            loop.create_task(callback())

            return unsubscribe

        # noinspection PyUnresolvedReferences
        return reactivex.create(subscribe)

    def on_property_change(self, td, name):
        """Subscribes to property changes on a remote Thing.
        Returns an Observable"""

        href = self.pick_http_href(td, td.get_property_forms(name), op=InteractionVerbs.OBSERVE_PROPERTY)

        if href is None:
            raise FormNotFoundException()

        def subscribe(observer, scheduler):
            """Subscription function to observe property updates using the HTTP protocol."""

            state = {"active": True}

            @handle_observer_finalization(observer)
            async def callback():
                http_client = tornado.httpclient.AsyncHTTPClient()
                http_request = tornado.httpclient.HTTPRequest(href, method="GET", validate_cert=False)

                while state["active"]:
                    try:
                        response = await http_client.fetch(await self.sign_request(http_request))
                        value = json.loads(response.body)
                        value = value.get("value", value)
                        init = PropertyChangeEventInit(name=name, value=value)
                        observer.on_next(PropertyChangeEmittedEvent(init=init))
                    except HTTPTimeoutError:
                        pass

            def unsubscribe():
                state["active"] = False

            loop = asyncio.get_running_loop()
            loop.create_task(callback())

            return unsubscribe

        # noinspection PyUnresolvedReferences
        return reactivex.create(subscribe)

    def on_td_change(self, url):
        """Subscribes to Thing Description changes on a remote Thing.
        Returns an Observable."""

        raise NotImplementedError
