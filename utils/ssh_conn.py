# -*- coding: utf-8 -*-

import os

import paramiko


def ssh_conn(workdir, filename, host, user, passwd, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, passwd, timeout=3)
    stdin, stdout, stderr = ssh.exec_command('file' + ' ' + filename)
    ssh.close()
