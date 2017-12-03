#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmsapp

CallLegStatus = {'waitPINcode': 0, 'inConf': 1}


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
    def __init__(self):
        # xmsapp.XMSAPP.__init__(host='10.10.11.15', port=81, name='app')
        super(Conference, self).__init__()
        self.calls = {}
        self.pincode = '123456'
        self.confroom = None

    def On_Incomming(
            self, resource_type, resource_id, call_id, called_uri, caller_uri):
        self.Answer_Call(resource_type, resource_id)
        self.calls[resource_id] = CallLeg(resource_type, resource_id, call_id)
        # TODO play "please input the PIN Code"
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
                        status_code, reasonm, conf_href, conf_identifier = \
                            self.Create_Conf(max_parties=4)
                        if status_code == 201:
                            self.confroom = \
                                ConfRoom(conf_href, conf_identifier)
                    self.Add_Party(
                            resource_type, resource_id,
                            self.confroom.conf_identifier)
                    callLeg.status = CallLegStatus['inConf']
                    self.confroom.paryies[resource_id] = resource_id
                    # TODO play welcome message
                    pass
                else:
                    # TODO play "wrong PIN code, byebye."
                    self.Drop_Call(resource_type, resource_id)
                    del self.calls[resource_id]
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
                # TODO play some leave message
                if len(self.confroom.paryies) == 0:
                    self.Drop_Conf("", self.confroom.conf_identifier)
                    self.confroom = None
                pass
            del self.calls[resource_id]


if __name__ == '__main__':
    appclient = Conference()
    appclient.Get_AllCallResources()
    appclient.Create_EventHandler()
    appclient.Retrieve_Events()
