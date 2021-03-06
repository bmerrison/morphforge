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

from morphforge.simulation.base import CurrentClamp
from neuronobject import NEURONObject
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.core.quantities import unit
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforge.simulation.neuron.hocmodbuilders import HocBuilder
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable
from morphforge.simulation.base.stimulation import CurrentClampStepChange
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment


class CurrentClampCurrentRecord(NEURONRecordable):

    def __init__(self, cclamp, **kwargs):
        super(CurrentClampCurrentRecord, self).__init__(**kwargs)
        self.cclamp = cclamp

    def get_unit(self):
        return unit('nA')

    def get_std_tags(self):
        return [StandardTags.Current]

    def build_hoc(self, hocfile_obj):
        name_hoc = hocfile_obj[MHocFileData.CurrentClamps][self.cclamp]['stimname']
        HocModUtils.create_record_from_object(
                        hocfile_obj=hocfile_obj,
                        vecname='RecVec%s' % self.name, 
                        objname=name_hoc,
                        objvar='i',
                        recordobj=self)

    def build_mod(self, modfile_set):
        pass

    def get_description(self):
        return 'Current Clamp Injection: %s' % self.cclamp.name



class NEURONCurrentClampStepChange(CurrentClampStepChange, NEURONObject):

    def __init__(self, **kwargs):
        super(NEURONCurrentClampStepChange, self).__init__(**kwargs)

    def build_hoc(self, hocfile_obj):
        HocBuilder.CurrentClamp(hocfile_obj=hocfile_obj,
                                currentclamp=self)

    def build_mod(self, modfile_set):
        pass

    def get_recordable(self, what, name=None, **kwargs):
        recorders = {
            CurrentClamp.Recordables.Current: CurrentClampCurrentRecord
        }

        return recorders[what](cclamp=self, name=name, **kwargs)


NEURONEnvironment.currentclamps.register_plugin(CurrentClampStepChange, NEURONCurrentClampStepChange)
