#!/usr/bin/env python

########################################################################################################################
#									Load configuration information for the updater daemon							   #
########################################################################################################################
#																		(C) Manuel Bernal Llinares <mbdebian@gmail.com>#
#																			Distributed under the Apache License 2.0   #
########################################################################################################################

_config = None

import os
import json
import sys
import optparse
import uuid
import time

_config = None


def prepareConfig():
    global _config
    # print("Preparing config")
    configFile = "./config.updater.json"
    # Parse command line options
    # Create the command line parser with its options
    cmdl_version = '2015.03.05'
    cmdl_parser = optparse.OptionParser(version=cmdl_version, conflict_handler='resolve')
    cmdl_parser.add_option('-h', '--help', action='help', help='print this help text and exit')
    cmdl_parser.add_option('-v', '--version', action='version', help='print program version and exit')
    cmdl_parser.add_option('-c', '--config', dest='configFileName', metavar='PATH_TO_CONFIG_FILE',
                           help='specify a config file to use for the session')
    (cmdl_options, cmdl_args) = cmdl_parser.parse_args()

    if cmdl_options.configFileName:
        configFile = cmdl_options.configFileName

    # print("Reading config file " + configFile)

    # Load config file
    with open(configFile) as cf:
        _config = json.load(cf)
    _config['config'] = {}
    _config['config']['file'] = configFile

    # Setup logging settings
    currentTime = time.localtime()
    if "logger" not in _config:
        _config['logger'] = {}
    if "folder" not in _config['logger']:
        _config['logger']['folder'] = './'
    if "namespace" not in _config['logger']:
        _config['logger']['namespace'] = 'updater'
    if "filePath" not in _config['logger']:
        _config['logger']['filePath'] = _config['logger']['folder'] \
                                        + "/" + "update-" + str(currentTime.tm_year) \
                                        + format(currentTime.tm_mon, "02") \
                                        + format(currentTime.tm_mday, "02") \
                                        + "_" \
                                        + format(currentTime.tm_hour, "02") \
                                        + "." \
                                        + format(currentTime.tm_min, "02") \
                                        + "." \
                                        + format(currentTime.tm_sec, "02") \
                                        + ".log"
    if "ouputAndErrorFilePath" not in _config['logger']:
        _config['logger']['ouputAndErrorFilePath'] = _config['logger']['filePath'] + ".out"


def getConfig():
    global _config
    if not _config:
        prepareConfig()
    return _config


def main():
    print("This module is not designed to be run alone")


if __name__ == "__main__":
    main()
