
from .thirdparty.telnetsrv.green import TelnetHandler, command
from gevent.server import StreamServer
from os import R_OK, W_OK
from lxml import etree
import conpot.core as conpot_core
from gevent.server import StreamServer
from conpot.core.protocol_wrapper import conpot_protocol
from datetime import datetime
import logging

BANNER = """
----------------------------------------


Service Fullfillment Center
Sri Lanka Telecom PLC
Config by       : D.M.U.P Karunarathne
Date            : 22/01/2014
Type            : C891F
S/N             : FGL222992A7
Service         : D-BIL
Customer        : VISTA G CONSULT PVT LTD
CIRCUIT ID      : D81249 (Old_D82300)
Modified	: K.S.Perera (16/06/2019)
----------------------------------------

User Access Verification
"""

class TELNETHandler(TelnetHandler):
    WELCOME = "You're now logged as admin!"
    TELNET_ISSUE = BANNER#"\n\n\nWelcome to R230aw version V.7.10 Rev. 1 (Patch 3) IPSec from 2012/04/24 00:00:00\nsystemname is Bartoccini Spoleto, location Bartoccini Spoleto\n\n"
    authNeedUser = 'admin'
    authNeedPass = 'admin'
    MAX_AUTH_ATTEMPTS = 3
    PROMPT = "$ "
    authNeedUser = 'admin'
    authNeedPass = 'admin'
    process = None


    def authCallback(self, username, password):
        '''Called to validate the username/password.'''
        # logging credentials
        #if username is not None and password is not None:
        #    self._log("AUTH", "%s:%s" % (username, password))

        if not(username == 'admin' and password == 'admin'):
            raise Exception("[x] wrong credentials ('%s':'%s')" % (username, password))


    @command(['echo', 'copy', 'repeat'])
    def command_echo(self, params):
        '''<text to echo>
        Echo text back to the console.

        '''
        self.writeresponse( ' '.join(params) )

    @command('timer')
    def command_timer(self, params):
        '''<time> <message>
        In <time> seconds, display <message>.
        Send a message after a delay.
        <time> is in seconds.
        If <message> is more than one word, quotes are required.
        example:
        > TIMER 5 "hello world!"
        '''
        try:
            timestr, message = params[:2]
            time = int(timestr)
        except ValueError:
            self.writeerror( "Need both a time and a message" )
            return
        self.writeresponse("Waiting %d seconds...", time)
        thirdparty.gevent.spawn_later(time, self.writemessage, message)


class TELNETConfig(TelnetHandler):
    def __init__(self, template):
        dom = etree.parse(template)
        # retrieve protocol configuration for specified device
        self.device_type = (dom.xpath('//telnet/device_info/device_type/text()'))[0]
        BANNER = (dom.xpath('//telnet/device_info/banner/text()'))[0]
        self.max_login_attemps = int((dom.xpath('//telnet/device_info/max_login_attemps/text()'))[0])
        
        if dom.xpath('//telnet/device_info/motd/text()'):
            self.motd = (dom.xpath('//telnet/device_info/motd/text()'))[0]
        else:
            self.motd = None


class TELNETServer(object):
    def __init__(self, template, template_directory, args):
        self.template = template
        self.template_directory = template_directory
        self.server = None          # Initialize later

        # Initialize vfs here..
        self.handler = TELNETHandler
        self.handler.config = TELNETConfig(self.template)

    def start(self, host, port):
        self.handler.host, self.handler.port = host, port
        connection = (self.handler.host, self.handler.port)
        self.server = StreamServer(connection, self.handler.streamserver_handle)
        #logger.info('TELNET server started on: {}'.format(connection))
        print('TELNET server started on: {}'.format(connection))
        self.server.serve_forever()

    def stop(self):
        #logger.debug('Stopping TELNET server')
        print('Stopping TELNET server')
        self.server.stop()
        del self.handler


# ---- For debugging ----
if __name__ == '__main__':
    # Set vars for connection information
    TCP_IP = '127.0.0.1'
    TCP_PORT = 10002
    import os
    import conpot
    import conpot.core as conpot_core
    dir_name = os.path.dirname(conpot.__file__)
    print(dir_name)
    conpot_core.get_databus().initialize(dir_name + "/templates/default/template.xml")
    server = TELNETServer(
        dir_name + "/templates/default/telnet/telnet.xml",
        dir_name + "/templates/default/",
        None,
    )
    #server = TELNETServer(test_template, None, None)
    try:
        server.start(TCP_IP, TCP_PORT)
    except KeyboardInterrupt:
        server.stop()