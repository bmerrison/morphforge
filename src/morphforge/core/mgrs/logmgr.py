#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import logging
import os
import inspect


class LogMgrState(object):
    Ready = "Ready"
    Configuring = "Configuring"
    Uninitialised = "Uninitalised"


class LogMgr(object):

    initState = LogMgrState.Uninitialised
    loggers = {}


    @classmethod
    def config(cls):
        from locmgr import LocMgr

        if cls.initState == LogMgrState.Configuring: return
        if cls.initState == LogMgrState.Ready: return


        cls.initState = LogMgrState.Configuring

        logfilename = os.path.join(LocMgr.get_log_path(), "log.html")
        logging.basicConfig(filename=logfilename, level=logging.INFO)

        cls.initState = LogMgrState.Ready

        cls.info_from_logger("Logger Started OK")



    @classmethod
    def _pyfile_to_modulename(cls, filename):
        localPath = filename
        morphforgeLib = False
        if "morphforge" in filename:
            localPath = "morphforge" + filename.split("morphforge")[-1]
            morphforgeLib = True
        localPath = localPath.replace(".py", "")
        localPath = localPath.replace("/", ".")
        return localPath, morphforgeLib


    @classmethod
    def get_caller(cls):
        currentFrame = inspect.currentframe()
        outerFrames = inspect.getouterframes(currentFrame)
        outFramesNotThisClass = [f for f in outerFrames if not f[1].endswith("logmgr.py") ]

        prevCallFrame = outFramesNotThisClass[0]
        caller = cls._pyfile_to_modulename(prevCallFrame[1])
        return caller, prevCallFrame[2]

    @classmethod
    def info_from_logger(cls, msg):
        packageName = "morphforge.core.logmgr"
        if not packageName in cls.loggers:
            cls.loggers[packageName] = cls.create_logger(packageName)
        cls.loggers[packageName].info(msg)





    @classmethod
    def _is_logging_active_and_ready(cls):


        if cls.initState == LogMgrState.Ready:
            from settingsmgr import SettingsMgr
            if not SettingsMgr.is_logging(): return False
            return True
        elif cls.initState == LogMgrState.Configuring: return False
        elif cls.initState == LogMgrState.Uninitialised:
            cls.config()
            return True
        else:
            raise ValueError()



    @classmethod
    def info(cls, msg):
        if not cls._is_logging_active_and_ready(): return
        cls.get_logger().info(msg)


    @classmethod
    def debug(cls, msg):
        if not cls._is_logging_active_and_ready(): return
        cls.get_logger().debug(msg)

    @classmethod
    def warning(cls, msg):
        if not cls._is_logging_active_and_ready(): return
        cls.get_logger().warning(msg)





    @classmethod
    def create_logger(cls, logName):
        logger = logging.getLogger(logName)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        return logger


    @classmethod
    def get_logger(cls):

        # Find Who called us:
        callMod = "DISABLEDLOGGING"
        #(callMod, isMorphforgeLib), lineNum = cls.get_caller()


        if not callMod in cls.loggers:
            cls.loggers[callMod] = cls.create_logger(callMod)
        return cls.loggers[callMod]


