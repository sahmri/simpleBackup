# simpleBackup
A few python scripts implementing a simple backup strategy.
It was initially developed for Mac and Linux machines, and it uses rsync in the background.

# How to setup the daemons
There are two main scripts
  - mainDaemon.py, this is in charge of doing the backups according to what it says in the configuration file.
  - updateme.py, this script can be set up on CRON to periodically look for updates of the code, it basically runs
    a pull request on the GIT repository.
    
# Backups config file
In JSON format, contains several main sections:
  - credentials, used to access to servers, all authentication is RSA based, so no passwords are used
  - servers, contains information about the servers that we want to use for the backups
  - backups, contains one entry 'key': {entry_data}, per item we want to backup
    - backup entry, contains the following information
      - name, of this backup item
      - description, some useful information that could be used in log reports about this backup item
      - source, this is the source data of the backup
      - destination, destination of the backup. Both, source and destination, can be remote or local endpoints
      - signalFiles, can be used with a local or a remote source/destination, and it represents a list of empty files
        the backup daemon will create (touch) after a successful backup of the current item.
