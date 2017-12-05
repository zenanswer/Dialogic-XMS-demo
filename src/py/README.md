File list
===

-   xmsrest.xsd - Dialogic XMS RESTFull Body Payload Schema Definition
-   xmsrest.py - Data Struct Definition for Python, be generated from "xmsrest.xsd"
-   xmsapp.py - Python wrapper for Dialogic XMS RESTFull API
-   earlymediaandplay.py - Sample code for showing early-media, play audio and play&collect.
-   conference.py - Sample code for conference room
-   conference_clear.py - Sample code for clear all conference room
-   restfulmgmtapitest.py - Sample code for using XMS Management API
-   README.md - README file

Dialogic XMS XSD file for RESTFull API
===

 Location

```bash
[root@xms01 ~]# ls -lt /etc/xms/xmsrest.xsd
-rw-r--r--. 1 root root 54704 Nov 15 13:45 /etc/xms/xmsrest.xsd
[root@xms01 ~]#
```

Generate Python data struct from XSD file
===

[generateDS 2.28.2](https://pypi.python.org/pypi/generateDS/)

Command line:

```bash
[root@xms01 ~]$ generateDS.py -o xmsrest.py xmsrest.xsd
```
