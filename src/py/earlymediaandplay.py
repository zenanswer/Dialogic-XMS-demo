#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmsapp


class EarlyMediaAndPlay(xmsapp.XMSAPP):

    def On_Incomming(
            self, resource_type, resource_id, call_id, called_uri, caller_uri):
        self.Accept_Call(resource_type, resource_id)
        self.Play(
                resource_type, resource_id,
                'file://verification/verification_intro.wav')

    def On_PlayEnd(self, resource_type, resource_id, reason, digits):
        if not hasattr(self, 'answered') or not self.answered:
            self.Answer_Call(resource_type, resource_id)
            self.answered = True
            self.Play_Collect(
                    resource_type, resource_id,
                    'file://verification/verification_intro.wav', 4)

    def On_Hangup(self):
        self.answered = False


if __name__ == '__main__':
    appclient = EarlyMediaAndPlay()
    appclient.Get_AllCallResources()
    appclient.Create_EventHandler()
    appclient.Retrieve_Events()
