#!/usr/bin/env python3
# encoding: utf-8

"""
@author: wangchao44
@Date: 2021/2/4 17:30
@desc:
======================


======================
"""

# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: record failed task name
    callback_type: notification
    requirements:
      - whitelist in configuration
    short_description: sends JSON events to syslog
    version_added: "2.6"
    description:
      - record the last failed task, used for retry with start-at-task
    options:
        N/A
'''

import os
import json
import logging
import logging.handlers
import socket

from ansible.plugins.callback import CallbackBase

FILE_RECORD_FAILED_TASK = "/var/log/ansible_failed_task.log"

class CallbackModule(CallbackBase):
    """
    logs ansible-playbook and ansible runs to a syslog server in json format
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'record_failed_task'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):

        super(CallbackModule, self).__init__()

        self.logger = logging.getLogger('ansible record')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.handlers.SysLogHandler("/dev/log")
        self.logger.addHandler(self.handler)
        self.hostname = socket.gethostname()

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task = result.task_name
        self.logger.info("record failed task name: {}".format(task))
        with open(FILE_RECORD_FAILED_TASK, "w") as f:
            f.write(task)