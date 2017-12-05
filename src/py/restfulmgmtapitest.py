#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json


def MgmAPi(rul, user='admin', password='admin'):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'}
    response = requests.get(
        rul,
        headers=headers,
        auth=requests.auth.HTTPBasicAuth(user, password),
        # for disable CERTIFICATE_VERIFY_FAILED error
        verify=False)
    print response.status_code, response.reason
    # print response.text
    return (response.status_code, response.text)


if __name__ == '__main__':
    status_code, body = MgmAPi('https://10.10.11.15:10443')
    decoded = json.loads(body, 'utf-8')
    if u'resources' in decoded:
        for resource in decoded[u'resources']:
            if u'uri' in resource:
                print 'Resource:', resource[u'uri']

    status_code, body = MgmAPi('https://10.10.11.15:10443/resource/active')
    decoded = json.loads(body, 'utf-8')
    print decoded
