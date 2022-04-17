# -*- coding: utf-8 -*-
import socket
import os
import getpass
from pathlib import Path

from _thread import *

from wildchildanimation.gui.swing_utils import write_log

PROPERTIES_FILE = "studioplugin.json"

KITSU_HOST = "https://production.wildchildanimation.com/api"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 18099

BYTE_SIZE = 1024
BACKLOG = 5

COMMAND_BYE    = "#bye#"
COMMAND_STRING = "#cmd#"
PUBLISH_ASSET = "publish_asset#"

HEADER_LENGTH = 5

from PyQt5 import QtCore

import sys
import json
import traceback

def normalize(item):
    if "id" in item:
        return item["id"]
    return item

def get_preferences_file():
    return Path.home() / PROPERTIES_FILE    

def load_properties():
    properties = {}
    properties_file = get_preferences_file()

    # write_log("preference file", properties_file)

    if properties_file.exists():
        # write_log("preference file", properties_file)

        with properties_file.open() as json_file:
            try:
                properties = json.load(json_file)
                # write_log("preference file", "loaded", properties_file)
            except:
                write_log("preference file", "created", properties_file)
                traceback.print_exc(file=sys.stdout)
                properties = {}
            # try to load json file
        # try to open json file

    # otherwise, reinit ---
    if not "server" in properties:
        properties["server"] = KITSU_HOST

    if not "username" in properties:
        properties["username"] = getpass.getuser()

    if not "token" in properties:
        properties["token"] = ""

    if not "port" in properties:
        properties["port"] = DEFAULT_PORT

    if not "host" in properties:
        properties["host"] = DEFAULT_HOST

    if not "separator" in properties:
        properties["separator"] = os.path.sep

    return properties
### load properties file local user preferences, re-init json if corrupt / not found    

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TCP Interface to Studio Tools Gui
class ThreadedServer(QtCore.QThread):
    loaded = QtCore.pyqtSignal(object)

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # main workflow
    def process(self, document):
        ## write_log("PathHelper", self.path_helper.get_paths())

        data = json.loads(document)

        ##write_log(app, client, args, command)
        return { "status": "Not Implemented Yet", "data": data }

    def __init__(self, address, props, task_status_signal = None):
        QtCore.QThread.__init__(self)

        self.address = address
        self.properties = props

        try:
            self.task_status_signal = task_status_signal
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.address)
            self.socket.listen()
            self.may_run = True
            write_log("server::created", self.address, BACKLOG)
        except Exception as inst:
            self.may_run = False
            write_log("************************************************************")
            write_log("**ERROR**", address, "\r\n***\r\n")
            write_log("************************************************************")
            write_log("\n\n")
            traceback.print_exc(file=sys.stdout)
            write_log("\n\n")
            write_log("************************************************************")
        return

    def __del__(self):
        self.wait()

    def stop(self):
        self.may_run = False
        self.terminate()

    def run(self):
        while self.may_run:
            write_log("threadedserver::threaded_execute", "waiting")

            client, addr = self.socket.accept()
            try:
                try:
                    self.threaded_execute(client)
                except Exception as inst:
                    write_log("************************************************************")
                    write_log("Command Error: let's see what happened ...")
                    write_log("************************************************************")
                    write_log("\n\n")

                    write_log(type(inst))
                    write_log(inst.args)
                    write_log(inst)

                    traceback.print_exc(file=sys.stdout)

                    write_log("\n\n")
                    write_log("************************************************************")
                    write_log("That's all I know, sorry ... ")
                    write_log("************************************************************")
                # process
            finally:
                if (client):
                    client.close()
            # done


    def threaded_execute(self, client):
        # receive the data length from client
        write_log("server::execute::threaded_execute")
        data_bytes = client.recv(HEADER_LENGTH)
        write_log("server::execute::header", data_bytes)

        #client.send(data_bytes)

        expected = int(data_bytes)
        write_log("server::execute::header", "expecting", expected)

        data_bytes = client.recv(expected)
        write_log("server::execute::header", "received", len(data_bytes))

        data = data_bytes.decode('utf-8')
        ### write_log("server::execute", "\r\n", data, "\r\n")

        #if not data:
        #    print("bye")

        results = None
        try:
            results = self.process(data)
        except Exception as inst:
            write_log("************************************************************")
            write_log("Command Error: let's see what happened ...")
            write_log("************************************************************")
            write_log("\n\n")

            write_log(type(inst))
            write_log(inst.args)
            write_log(inst)

            traceback.print_exc(file=sys.stdout)

            write_log("\n\n")
            write_log("************************************************************")
            write_log("That's all I know, sorry ... ")
            write_log("************************************************************")
        # pass

        #if COMMAND_STRING in data:
        #    self.run_command(data, client)
        write_log("server::execute::result", "size", len(results))
        RuntimeError("WhatTheFrek")

        # return { "status": "OK" }
        if "OK" in results["status"]:

            if not results["data"]:
                write_log("server::execute::result", "size", len(results))

                message_length = str(len(COMMAND_BYE)).zfill(HEADER_LENGTH)
                client.sendall(message_length.encode('utf-8'))
                client.sendall(COMMAND_BYE.encode('utf-8'))
            else:
                write_log("server::execute::result", "size", len(results))
                data = results["data"]
                message = json.dumps(data)
                message_length = str(len(message)).zfill(HEADER_LENGTH)

                write_log("server results", "length", message_length)

                client.sendall(message_length.encode('utf-8'))
                client.sendall(message.encode('utf-8'))
        else:
            # should send an error message here
            message_length = str(len(COMMAND_BYE)).zfill(HEADER_LENGTH)
            client.sendall(message_length.encode('utf-8'))
            client.sendall(COMMAND_BYE.encode('utf-8'))

        client.close()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


class SwingServer(object):

    ### #########################################################################
    def load_data(self, command = None, args = None):
        data = {}
        data["application"] = {}
        data["application"]["client"] = "studio-agent"
        data["application"]["version"] = "1"
        data["application"]["separator"] = os.sep
        data["command"] = {}

        if (command):
            data["command"]["name"] = command

        data["args"] = {}
        if (args):
            for key, val in args:
                data["args"][key] = val

        return data

    def __init__(self, props, task_status_signal = None):
        self.properties = props
        self.task_status_signal = task_status_signal
        self.address = (self.properties["host"], int(self.properties["port"]))
        self.running = False
        self.server = ThreadedServer(self.address, self.properties, self.task_status_signal)

    def normalize(self, item):
        if "id" in item:
            return item["id"]
        return item

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

if __name__ == "__main__":
    write_log("starting test server on port 18099")
    server = SwingServer(load_properties())
    server.start()
    write_log("done starting test server on port 18099")
