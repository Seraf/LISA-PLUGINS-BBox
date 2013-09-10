# -*- coding: UTF-8 -*-
import json, os, inspect
from pymongo import MongoClient
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from time import time, sleep
from lisa import configuration

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='bbox', localedir=path, languages=[configuration['lang']]).ugettext

class SNMP:
    def __init__(self):
        self.startedAt = time()
        # Protocol version to use
        self.pMod = api.protoModules[api.protoVersion2c]
        # Build PDU
        self.reqPDU = self.pMod.SetRequestPDU()

    def cbTimerFun(self, timeNow):
        if timeNow - self.startedAt > 3:
            raise Exception("Request timed out")

    def cbRecvFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=self.pMod.Message())
            rspPDU = self.pMod.apiMessage.getPDU(rspMsg)
            # Match response to request
            if self.pMod.apiPDU.getRequestID(self.reqPDU) == self.pMod.apiPDU.getRequestID(rspPDU):
                # Check for SNMP errors reported
                errorStatus = self.pMod.apiPDU.getErrorStatus(rspPDU)
                if errorStatus:
                    print(errorStatus.prettyPrint())
                transportDispatcher.jobFinished(1)
        return wholeMsg

    def send(self, host, community, oid, value):
        self.pMod.apiPDU.setDefaults(self.reqPDU)
        self.pMod.apiPDU.setVarBinds(
            self.reqPDU,
            ((oid, self.pMod.OctetString(value)),
            )
        )

        # Build message
        reqMsg = self.pMod.Message()
        self.pMod.apiMessage.setDefaults(reqMsg)
        self.pMod.apiMessage.setCommunity(reqMsg, community)
        self.pMod.apiMessage.setPDU(reqMsg, self.reqPDU)

        transportDispatcher = AsynsockDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbRecvFun)
        transportDispatcher.registerTimerCbFun(self.cbTimerFun)

        # UDP/IPv4
        transportDispatcher.registerTransport(
            udp.domainName, udp.UdpSocketTransport().openClientMode()
        )

        # Pass message to dispatcher
        transportDispatcher.sendMessage(
            encoder.encode(reqMsg), udp.domainName, (host, 161)
        )
        transportDispatcher.jobStarted(1)

        # Dispatcher will finish as job#1 counter reaches zero
        transportDispatcher.runDispatcher()
        transportDispatcher.closeDispatcher()

class BBox:
    def __init__(self):
        self.configuration_lisa = configuration
        self.mongo = MongoClient(self.configuration_lisa['database']['server'],
                            self.configuration_lisa['database']['port'])
        self.configuration = self.mongo.lisa.plugins.find_one({"name": "BBox"})
        self.snmp = SNMP()
        self.answer = ""
        self.chaines = {
            "1": ["50"],
            "2": ["51"],
            "3": ["52"],
            "4": ["53"],
            "5": ["54"],
            "6": ["55"],
            "7": ["56"],
            "8": ["57"],
            "9": ["58"],
            "10": ["50","59"],
            "11": ["50","50"],
            "12": ["50","51"],
            "13": ["50","52"],
            "14": ["50","53"],
            "next": ["25"],
            "previous": ["26"]
        }

        self.volume_actions = {
            "up": ["27"],
            "down": ["28"]
        }

    def channel(self, jsonInput):
        #Send a stop to return to the live
        self.snmp.send( host=str(self.configuration['configuration']['ip']),
                        community=str(self.configuration['configuration']['community']),
                        oid=str(self.configuration['configuration']['oid']),
                        value=str("20")
        )
        sleep(1)
        print jsonInput['outcome']
        number = jsonInput['outcome']['entities']['bbox_chaine']['value']

        if number:
            for chaine in self.chaines[number]:
                self.snmp.send( host=str(self.configuration['configuration']['ip']),
                                community=str(self.configuration['configuration']['community']),
                                oid=str(self.configuration['configuration']['oid']),
                                value=str(chaine)
                )
        if jsonInput['outcome']['entities']['bbox_action_channel']['value'] == "pause":
            sleep(8)
            self.snmp.send( host=str(self.configuration['configuration']['ip']),
                            community=str(self.configuration['configuration']['community']),
                            oid=str(self.configuration['configuration']['oid']),
                            value=str("23")
            )
            self.answer = _('channel_pausing')
        elif jsonInput['outcome']['entities']['bbox_action_channel']['value'] == "record":
            #Send REC
            self.snmp.send( host=str(self.configuration['configuration']['ip']),
                            community=str(self.configuration['configuration']['community']),
                            oid=str(self.configuration['configuration']['oid']),
                            value=str("24")
            )
            sleep(2)
            #Send OK
            self.snmp.send( host=str(self.configuration['configuration']['ip']),
                            community=str(self.configuration['configuration']['community']),
                            oid=str(self.configuration['configuration']['oid']),
                            value=str("7")
            )
            self.answer = _('channel_recording')
        else:
            self.answer = _('channel_changed')
        return {"plugin": "BBox",
                "method": "channel",
                "body": self.answer
        }

    def volume(self, jsonInput):
        action = jsonInput['outcome']['entities']['bbox_action_volume']['value']
        for order in self.volume_actions[action]:
            self.snmp.send( host=str(self.configuration['configuration']['ip']),
                            community=str(self.configuration['configuration']['community']),
                            oid=str(self.configuration['configuration']['oid']),
                            value=str(order)
            )
        if action == "up":
            self.answer = ' '.join([_('Volume'),_('increased')])
        else:
            self.answer = ' '.join([_('Volume'),_('decreased')])

        return {"plugin": "BBox",
                "method": "volume",
                "body": self.answer
        }