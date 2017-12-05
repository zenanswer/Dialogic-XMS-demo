#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmsapp


class MRCPTest(xmsapp.XMSAPP):
    pass


testapp = MRCPTest()
status_code, reason, mrcp_href, mrcp_identifier = testapp.Create_MRCP()
# testapp.Drop_MRCP()
