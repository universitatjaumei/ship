#!/usr/bin/python2

import argparse
import os
import sys
import re

import requests
import codecs
import os

URL = 'http://conf.uji.es/v2/keys/ujiapps/apps/%s/app.properties'

class AppsProperties:

    def __init__(self, app):
        self.app = app

    def get(self):
        r = requests.get(URL % self.app)
        data = r.json()
        if data.get("node") and data.get("node").get("value"):
            return data["node"]["value"]
        else:
            return ''

    def create_app_properties_directory(self):
        try:
            os.makedirs("/etc/uji/%s" % self.app)
        except Exception as e:
            pass

    def save_todisk(self):
        self.create_app_properties_directory()
        with codecs.open("/etc/uji/%s/app.properties" % self.app, "w+", "utf-8") as properties_file:
            properties_file.write(self.get())

    def save(self, properties):
        requests.put(URL % self.app, data={"value": properties})

    def new(self):
        properties = self.get()

        if properties != "":
            raise Exception("App already exists")

        self.save('')



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Import an app.properties file into config.uji.es")
    parser.add_argument("-a", "--app", help="Application acronym")
    parser.add_argument("app_properties_file", help="app.properties file location")
    args = parser.parse_args()

    appfile = args.app_properties_file
    appAcronym = args.app

    if not appAcronym:
        app_search = re.search("\/etc\/uji\/([a-zA-Z0-9]+)\/", appfile)
        if not app_search:
            print "APP not found, please specify APP acronym."
            sys.exit(-2)
        appAcronym = app_search.group(1)    
    
    if not os.path.exists(appfile):
        print "Filename not found."
        sys.exit(-1)

    with open(appfile) as f:
        properties = f.read()
        app = AppsProperties(appAcronym)
        app.save(properties)
