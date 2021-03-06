#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

import ConfigParser
import os


class RCMgr(object):

    _rc_filename = os.path.expanduser('~/.morphforgerc')
    _rc_config_parser = None

    @classmethod
    def has_config(cls):
        return os.path.exists(cls._rc_filename)

    @classmethod
    def get_config(cls):
        if not cls._rc_config_parser:
            cls._rc_config_parser = ConfigParser.SafeConfigParser()
            if not os.path.exists(cls._rc_filename):
                raise Exception("The resource file: %s does not exist!" % cls._rc_filename)
            cls._rc_config_parser.read([cls._rc_filename])
        return cls._rc_config_parser

    # Expose the same interface as the config parser does:
    @classmethod
    def has(cls, section, option):
        return cls.get_config().has_option(section, option)

    @classmethod
    def get(cls, section, option):

        # Allow building on RTD:
        on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
        if on_rtd:
            return ''

        return cls.get_config().get(section, option)


