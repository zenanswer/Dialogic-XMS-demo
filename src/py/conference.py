#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmsapp

CallLegStatus = {'waitPINcode': 0, 'inConf': 1}


class MRCP(object):
    def __init__(self, mrcp_href, mrcp_identifier):
        self.mrcp_href = mrcp_href
        self.mrcp_identifier = mrcp_identifier


class ConfRoom(object):
    def __init__(self, conf_href, conf_identifier):
        self.conf_href = conf_href
        self.conf_identifier = conf_identifier
        self.paryies = {}


class CallLeg(object):
    def __init__(self, resource_type, resource_id, call_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.call_id = call_id
        self.status = CallLegStatus['waitPINcode']


class Conference(xmsapp.XMSAPP):
    def __init__(self, host='10.10.11.15'):
        # xmsapp.XMSAPP.__init__(host='10.10.11.15', port=81, name='app')
        super(Conference, self).__init__(host=host)
        self.calls = {}
        self.pincode = '123456'
        self.confroom = None
        self.mrcptts = None

    def Clear_All(self):
        if (self.mrcptts is not None):
            self.Drop_MRCP('mrcp', self.mrcptts.mrcp_identifier)
        if (self.confroom is not None):
            for party in self.confroom.paryies:
                self.Drop_Call('call', party)
            self.Drop_Conf('conference', self.confroom.conf_identifier)

    def On_Incomming(
            self, resource_type, resource_id, call_id, called_uri, caller_uri):
        self.Answer_Call(resource_type, resource_id)
        self.calls[resource_id] = CallLeg(resource_type, resource_id, call_id)
        # play "please input the PIN Code"
        self.Play_Collect(
                resource_type, resource_id,
                'file://verification/verification_intro.wav', 6)

    def On_PlayEnd(self, resource_type, resource_id, reason, digits):
        if (resource_type == 'call'):
            callLeg = self.calls[resource_id]
            if callLeg is None:
                return
            if callLeg.status == CallLegStatus['waitPINcode']:
                # if digits is not None and digits == self.pincode:
                if digits is not None and len(digits) > 3:
                    if self.confroom is None:
                        # create conference
                        status_code, reason, conf_href, conf_identifier = \
                            self.Create_Conf(max_parties=4)
                        if status_code == 201:
                            self.confroom = \
                                ConfRoom(conf_href, conf_identifier)
                        # create MRCP for TTS
                        status_code, reason, mrcp_href, mrcp_identifier = \
                            self.Create_MRCP(True, True)
                        if status_code == 201:
                            self.mrcptts = \
                                MRCP(mrcp_href, mrcp_identifier)
                    if (self.confroom is not None
                            and self.confroom.conf_identifier is not None):
                        self.Add_Party(
                                resource_type, resource_id,
                                self.confroom.conf_identifier)
                        callLeg.status = CallLegStatus['inConf']
                        self.confroom.paryies[resource_id] = resource_id
                        if (self.mrcptts is not None
                                and self.mrcptts.mrcp_identifier is not None):
                            # play welcome message (TTS)
                            self.Speak(
                                'mrcp', self.mrcptts.mrcp_identifier,
                                'conference', self.confroom.conf_identifier,
                                'Someone came in, welcome.')
                else:
                    # play "wrong PIN code, byebye."
                    self.Play(
                            resource_type, resource_id,
                            'file://vxml/goodbye.wav')
                    del self.calls[resource_id]
                    self.Drop_Call(resource_type, resource_id)
                    pass

    def On_Hangup(self, resource_type, resource_id, reason):
        if (resource_type == 'call'):
            if resource_id not in self.calls:
                return
            callLeg = self.calls[resource_id]
            if callLeg.status == CallLegStatus['inConf']:
                self.Remove_Party(
                        resource_type, resource_id,
                        self.confroom.conf_identifier)
                del self.confroom.paryies[resource_id]
                if len(self.confroom.paryies) == 0:
                    self.Drop_Conf("", self.confroom.conf_identifier)
                    self.confroom = None
                else:
                    if (self.mrcptts is not None):
                        # play leave message (TTS)
                        self.Speak(
                            'mrcp', self.mrcptts.mrcp_identifier,
                            'conference', self.confroom.conf_identifier,
                            'Someone leaved.')
            del self.calls[resource_id]


if __name__ == '__main__':
    import signal
    import sys

    appclient = Conference()

    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        appclient.Clear_All()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    appclient.Get_AllCallResources()
    appclient.Create_EventHandler()
    appclient.Retrieve_Events()
