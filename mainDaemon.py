#!/usr/bin/env python

########################################################################################################################
#											Simple Backup System - Main Daemon										   #
########################################################################################################################
#																		(C) Manuel Bernal Llinares <mbdebian@gmail.com>#
#																			Distributed under the Apache License 2.0   #
########################################################################################################################

import os
import sys
import optparse
import settings
import logger
import json
import time
import subprocess


def getEndPoint(item):
    if item['type'] in "local":
        return item['folder'] + "/"
    elif item['type'] in "remote":
        config = settings.getConfig()
        return config['credentials'][item['credentials']]['user'] \
               + "@" + config['servers'][item['server']]['address'] \
               + ":" \
               + item['folder'] + "/"


def getSignalCommands(item):
    config = settings.getConfig()
    endPoints = []
    if "signalFiles" in item:
        if item['type'] in "local":
            for signal in item['signalFiles']:
                endPoints.append("touch " + signal)
        elif item['type'] in "remote":
            config = settings.getConfig()
            for signal in item['signalFiles']:
                endPoints.append("ssh " + config['credentials'][item['credentials']]['user'] \
                                 + "@" + config['servers'][item['server']]['address'] \
                                 + " touch " \
                                 + signal)
    return endPoints


def launchBackupForItem(bitem, key):
    config = settings.getConfig()
    miLogger = logger.getLogger()
    if 'disabled' in bitem:
        miLogger.warning("Skip DISABLED backup entry " + str(key))
        return None
    miLogger.info("Running backup for '" + bitem['name'] + "'")
    sourceEndPoint = getEndPoint(bitem['source'])
    destinationEndPoint = getEndPoint(bitem['destination'])
    command = "rsync -vahx -e ssh --no-devices --no-p " \
              + "--progress " \
              + "--stats " \
              + "--exclude=.Spotlight-V100 " \
              + "--exclude=.Trashes " \
              + "--exclude=.Trash " \
              + "--exclude=.fseventsd " \
              + "--exclude=._.Trashes " \
              + "--exclude=.DS_Store " \
              + "--exclude=._.DS_Store " \
              + sourceEndPoint \
              + " " \
              + destinationEndPoint \
              + " >> " + config['logger']['ouputAndErrorFilePath'] + " 2>&1"
    miLogger.debug("Synchronization command: " + command)
    return subprocess.Popen(command, shell=True)


def launchBackups():
    config = settings.getConfig()
    miLogger = logger.getLogger()
    # Run the backups
    ongoingBackups = {}
    for bitem in config['backups']:
        miLogger.debug("Processing backup entry " + bitem)
        ongoingBackups[bitem] = {'process': launchBackupForItem(config['backups'][bitem], bitem), 'tryCounter': 1}
    return ongoingBackups


def waitForBackupsToComplete(ongoingBackups):
    # Wait for them and repeat those with error state
    config = settings.getConfig()
    miLogger = logger.getLogger()
    signalCompletion = []
    ntries = 12
    while len(ongoingBackups) > 0:
        for bitem in list(ongoingBackups):
            if ongoingBackups[bitem]['process'] is None:
                ongoingBackups.pop(bitem, None)
                continue
            else:
            result = ongoingBackups[bitem]['process'].wait()
            if result:
                if ongoingBackups[bitem]['tryCounter'] == ntries:
                    miLogger.error("I've tried " + str(
                        ongoingBackups[bitem]['tryCounter']) + " times to run backup for " + bitem + ", " +
                                   config['backups'][bitem]['name'] + ", resulting in ERROR")
                    ongoingBackups.pop(bitem, None)
                else:
                    ongoingBackups[bitem]['tryCounter'] += 1
                    ongoingBackups[bitem]['process'] = launchBackupForItem(config['backups'][bitem], bitem)
            else:
                miLogger.info("Successful backup for " + config['backups'][bitem]['name'] + ", after trying it " + str(
                    ongoingBackups[bitem]['tryCounter']) + " times")
                ongoingBackups.pop(bitem, None)
                signalCompletion.append(bitem)
    return signalCompletion


def sendCompletionSignals(signalCompletion):
    config = settings.getConfig()
    miLogger = logger.getLogger()
    # Get the signaling commands
    ongoingSignals = {}
    for bitem in signalCompletion:
        commands = getSignalCommands(config['backups'][bitem]['source'])
        commands += getSignalCommands(config['backups'][bitem]['destination'])
        for command in commands:
            command = command + " >> " + config['logger']['ouputAndErrorFilePath'] + " 2>&1"
            ongoingSignals[bitem] = {'command': command, 'tryCounter': 1,
                                     'process': subprocess.Popen(command, shell=True)}
            miLogger.debug("Sending signal: " + command)

    # Wait for signal to complete
    ntries = 12
    while len(ongoingSignals) > 0:
        for bitem in list(ongoingSignals):
            result = ongoingSignals[bitem]['process'].wait()
            if result:
                if ongoingSignals[bitem]['tryCounter'] == ntries:
                    miLogger.error("I've tried " + str(
                        ongoingSignals[bitem]['tryCounter']) + " times to send the following signal " +
                                   ongoingSignals[bitem]['command'] + " for '" + config['backups'][bitem][
                                       'name'] + "', resulting in ERROR")
                    ongoingSignals.pop(bitem, None)
                else:
                    ongoingSignals[bitem]['tryCounter'] += 1
                    ongoingSignals[bitem]['process'] = subprocess.Popen(command, shell=True)
            else:
                miLogger.info(
                    "Successful signal sent for " + config['backups'][bitem]['name'] + ", after trying it " + str(
                        ongoingSignals[bitem]['tryCounter']) + " times")
                ongoingSignals.pop(bitem, None)


def main():
    # Get settings from file
    config = settings.getConfig()

    if config == None:
        print("Settings file could not be read from ")
        sys.exit(127)

    # Get logger
    miLogger = logger.getLogger()
    miLogger.info(str("=" * 120))
    miLogger.info("Backup session started")

    # Time the session
    sessionStart = time.time()

    # Do backups
    ongoingBackups = launchBackups()
    signalCompletion = waitForBackupsToComplete(ongoingBackups)
    sendCompletionSignals(signalCompletion)

    # Stop time
    sessionStop = time.time()
    m, s = divmod((sessionStop - sessionStart), 60)
    h, m = divmod(m, 60)
    miLogger.info("===> Total Time for the Session: " + "%d hours %02d minutes %02d seconds" % (h, m, s))

    # Session END, print resutls
    miLogger.info(str("=" * 120))


if __name__ == "__main__":
    main()
