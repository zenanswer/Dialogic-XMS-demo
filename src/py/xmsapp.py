#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import threading

import StringIO

import requests

import xmsrest


class XMSAPP(object):
    def __init__(self, host='10.10.11.15', port=81, name='app'):
        self.host = host
        self.port = port
        self.url = 'http://' + host + ":" + str(port)
        self.app = name
        self.eventhandlerhref = None
        self.__eventhandlers = {}
        self.__eventhandlers['keepalive'] = self.__handle_other
        self.__eventhandlers['stream'] = self.__handle_other
        self.__eventhandlers['media_started'] = self.__handle_other
        self.__eventhandlers['incoming'] = self.__handle_incoming
        self.__eventhandlers['end_play'] = self.__handle_end_play
        self.__eventhandlers['end_playcollect'] = self.__handle_end_play
        self.__eventhandlers['hangup'] = self.__handle_hangup

    def __handle_incoming(self, event_type, event):
        resource_type = event.get_event().get_resource_type()
        resource_id = event.get_event().get_resource_id()
        event_data = event.get_event().get_event_data()
        call_id = None
        called_uri = None
        caller_uri = None
        for data in event_data:
            if data.get_name() == 'call_id':
                call_id = data.get_value()
            if data.get_name() == 'called_uri':
                called_uri = data.get_value()
            if data.get_name() == 'caller_uri':
                caller_uri = data.get_value()
        print 'resource_type:', resource_type
        print 'resource_id:', resource_id
        print 'call_id:', call_id
        print 'called_uri:', called_uri
        print 'caller_uri:', caller_uri
        self.On_Incomming(
            resource_type, resource_id, call_id, called_uri, caller_uri)

    def Accept_Call(self, resource_type, resource_id):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        call = xmsrest.call(accept="yes", early_media="yes")
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()

        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Accept_Call ===='
        print response.status_code, response.reason
        print response.text

    def Answer_Call(self, resource_type, resource_id):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        call = xmsrest.call(answer="yes")
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()

        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Answer_Call ===='
        print response.status_code, response.reason
        print response.text

    def Drop_Call(self, resource_type, resource_id):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}
        response = requests.delete(self.url+path, params=payload)
        print '===== Drop_Call ===='
        print response.status_code, response.reason
        print response.text

    def Play(self, resource_type, resource_id, audio_file):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        play_source = xmsrest.play_source(
                audio_uri=audio_file, audio_type='audio/x-wav')
        play = xmsrest.play(play_source=play_source)
        call_action = xmsrest.call_action(play=play)
        call = xmsrest.call(call_action=call_action)
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()

        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Play ===='
        print response.status_code, response.reason
        print response.text

    def Play_Collect(self, resource_type, resource_id, audio_file, digit_num):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        timeout = 2

        play_source = xmsrest.play_source(
                audio_uri=audio_file, audio_type='audio/x-wav')
        playcollect = xmsrest.playcollect(
                play_source=play_source,
                cleardigits='yes',
                max_digits=str(digit_num),
                timeout=str(int(timeout*digit_num*1.5)) + 's',
                interdigit_timeout=str(timeout) + 's')
        call_action = xmsrest.call_action(playcollect=playcollect)
        call = xmsrest.call(call_action=call_action)
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()
        print '-------------'
        print data
        print '-------------'
        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Play_Collect ===='
        print response.status_code, response.reason
        print response.text

    def __handle_end_play(self, event_type, event):
        resource_type = event.get_event().get_resource_type()
        resource_id = event.get_event().get_resource_id()
        event_data = event.get_event().get_event_data()
        reason = None
        digits = None
        for data in event_data:
            if data.get_name() == 'reason':
                reason = data.get_value()
            if data.get_name() == 'digits':
                digits = data.get_value()
        print 'resource_type:', resource_type
        print 'resource_id:', resource_id
        print 'reason:', reason
        print 'digits:', digits
        self.On_PlayEnd(
            resource_type, resource_id, reason, digits)
        pass

    def __handle_hangup(self, event_type, event):
        resource_type = event.get_event().get_resource_type()
        resource_id = event.get_event().get_resource_id()
        event_data = event.get_event().get_event_data()
        call_id = None
        reason = None
        for data in event_data:
            if data.get_name() == 'call_id':
                call_id = data.get_value()
            if data.get_name() == 'reason':
                reason = data.get_value()
        print 'resource_type:', resource_type
        print 'resource_id:', resource_id
        print 'call_id:', call_id
        print 'reason:', reason
        self.On_Hangup(resource_type, resource_id, reason)

    def __handle_other(self, event_type, event):
        pass

    def Get_AllCallResources(self):
        path = '/default/calls'
        payload = {'appid': self.app}
        response = requests.get(self.url+path, params=payload)
        print '===== Get_AllCallResources ===='
        print response.text
        print '=' * 10
        response = xmsrest.parseString(response.text)
        # print response.calls_response.size
        if response.calls_response.size > '0':
            for call_response_item in response.calls_response.call_response:
                print '-' * 10
                print "destination_uri:" + call_response_item.destination_uri
                print "source_uri:" + call_response_item.source_uri
                print "href:" + call_response_item.href
                print "identifier:" + call_response_item.identifier

    def Create_EventHandler(self):
        path = '/default/eventhandlers'
        payload = {'appid': self.app}

        eventsubscribe = xmsrest.eventsubscribe()
        eventsubscribe.set_action("add")
        eventsubscribe.set_type("any")
        eventsubscribe.set_resource_id("any")
        eventsubscribe.set_resource_type("any")
        eventhandler = xmsrest.eventhandler(eventsubscribe=[eventsubscribe])
        web_service = xmsrest.web_service(eventhandler=eventhandler)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()
        print '===== Create_EventHandler Post Body===='
        print data
        print '=' * 10

        response = requests.post(self.url+path, params=payload, data=data)

        print '===== Create_EventHandler ===='
        print response.status_code, response.reason
        print response.text
        print '=' * 10
        if response.status_code == 201 and len(response.text) > 0:
            print '-' * 10
            response_body = xmsrest.parseString(response.text)
            print "identifier:" + \
                response_body.eventhandler_response.identifier
            print "href:" + \
                response_body.eventhandler_response.href
            self.eventhandlerhref = response_body.eventhandler_response.href

    def Retrieve_Events(self):
        path = self.eventhandlerhref
        payload = {'appid': self.app}
        print '===== Retrieve_Events ===='
        response = requests.get(self.url+path, params=payload, stream=True)
        print response.status_code, response.reason

        newline = unicode('\r\n', 'utf-8')
        pinding = unicode('', 'utf-8')
        chunksize = 0
        for raw_body in response.iter_content(
                chunk_size=256, decode_unicode=True):
            pinding = pinding + raw_body
            # print 'raw:', pinding.encode('utf-8')
            if chunksize == 0 and newline in pinding:
                chunksize_raw = pinding.split(newline)[0]
                pinding = pinding[len(chunksize_raw)+2:]  # inlcude \r\n
                chunksize = int(chunksize_raw, 16)
                print 'size:', chunksize
            if chunksize != 0:
                print 'len(pinding):', len(pinding)
                if len(pinding) < chunksize:
                    continue
                xmlbody = pinding[:chunksize]
                pinding = pinding[chunksize:]
                chunksize = 0
                print 'xml:', xmlbody
                self.__handle_event(xmlbody)

    def __handle_event(self, xmlstr):
        event = xmsrest.parseString(xmlstr)
        if (event.get_event() is not None
                and event.get_event().get_type() is not None):
            event_type = event.get_event().get_type()
            print '[EVENT]', event_type
            self.__eventhandlers[event_type](event_type, event)

    def On_Incomming(
            self, resource_type, resource_id, call_id, called_uri, caller_uri):
        pass

    def On_PlayEnd(
            self, resource_type, resource_id, reason, digits):
        pass

    def On_Hangup(self, resource_type, resource_id, reason):
        pass

    def Create_Conf(self, max_parties=60):
        path = '/default/conferences'
        payload = {'appid': self.app}

        conference = xmsrest.conference(max_parties=str(max_parties))
        web_service = xmsrest.web_service(conference=conference)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()
        print '-------------'
        print data
        print '-------------'
        http_response = requests.post(self.url+path, params=payload, data=data)
        print '===== Create_Conf ===='
        print http_response.status_code, http_response.reason
        print http_response.text
        conf_href = None
        conf_identifier = None
        response = xmsrest.parseString(http_response.text)
        if response.conference_response is not None:
            conf_href = response.conference_response.href
            conf_identifier = response.conference_response.identifier
            print '-' * 10
            print "href:" + conf_href
            print "identifier:" + conf_identifier
        return (
            http_response.status_code, http_response.reason,
            conf_href, conf_identifier)

    def Drop_Conf(self, resource_type, resource_id):
        path = '/default/conferences/' + resource_id
        payload = {'appid': self.app}
        response = requests.delete(self.url+path, params=payload)
        print '===== Drop_Conf ===='
        print response.status_code, response.reason
        print response.text

    def Add_Party(self, resource_type, resource_id, conf_identifier):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        add_party = xmsrest.add_party(
            conf_id=conf_identifier, caption=resource_id,
            audio="sendrecv", video="inactive")
        call_action = xmsrest.call_action(add_party=add_party)
        call = xmsrest.call(call_action=call_action)
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()

        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Add_Party ===='
        print response.status_code, response.reason
        print response.text

    def Remove_Party(self, resource_type, resource_id, conf_identifier):
        path = '/default/calls/' + resource_id
        payload = {'appid': self.app}

        remove_party = xmsrest.remove_party(conf_id=conf_identifier)
        call_action = xmsrest.call_action(remove_party=remove_party)
        call = xmsrest.call(call_action=call_action)
        web_service = xmsrest.web_service(call=call)
        web_service.set_version("1.0")
        output = StringIO.StringIO()
        web_service.export(output, 0)
        data = output.getvalue()

        response = requests.put(self.url+path, params=payload, data=data)
        print '===== Remove_Party ===='
        print response.status_code, response.reason
        print response.text


if __name__ == "__main__":
    appclient = XMSAPP()
    appclient.Get_AllCallResources()
    appclient.Create_EventHandler()
    appclient.Retrieve_Events()
