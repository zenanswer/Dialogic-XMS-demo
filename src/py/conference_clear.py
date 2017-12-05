#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmsapp


class ConfClear(xmsapp.XMSAPP):
    pass


testapp = ConfClear()
conferences = testapp.Get_AllConfResources()
for conf_id in conferences:
    testapp.Drop_Conf('conference', conf_id)
