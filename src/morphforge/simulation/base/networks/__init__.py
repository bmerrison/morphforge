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


class Synapse(object):

    class Recordables(object):

        SynapticCurrent = 'SynapticCurrent'
        SynapticConductance = 'SynapticConductance'

    def __init__(self, presynaptic_mech, postsynaptic_mech):
        self.preSynapticTrigger = presynaptic_mech
        self.postSynapticMech = postsynaptic_mech

        self.preSynapticTrigger = presynaptic_mech
        self.postSynapticMech = postsynaptic_mech

        self.postSynapticMech.synapse = self
        self.preSynapticTrigger.synapse = self

        self.population = None

    def get_presynaptic_mechanism(self):
        return self.preSynapticTrigger

    def get_postsynaptic_mechanism(self):
        return self.postSynapticMech

    def get_presynaptic_cell(self):
        return self.preSynapticTrigger.get_presynaptic_cell()

    def get_postsynaptic_cell(self):
        return self.postSynapticMech.get_postsynaptic_cell()


class GapJunction(object):

    def __init__(self, celllocation1, celllocation2, resistance, **kwargs):
        super(GapJunction, self).__init__(**kwargs)
        self.celllocation1 = celllocation1
        self.celllocation2 = celllocation2
        self.resistance = resistance

    @property
    def connected_cells(self):
        return [self.celllocation1.cell, self.celllocation2.cell]


class PreSynapticTypes(object):

    Cell = 'Cell'
    FixedTiming = 'Timing'


class PreSynapticMechanism(object):

    def __init__(self):
        self.synapse = None

    def get_presynaptic_cell(self):
        raise NotImplementedError()

    def get_type(self):
        raise NotImplementedError()


class PostSynapticMech(object):

    def __init__(self, cell_location, **kwargs):
        super(PostSynapticMech, self).__init__(**kwargs)
        self.cell_location = cell_location
        self.synapse = None
        #self.weight = weight

    def get_postsynaptic_cell(self):
        return self.cell_location.cell







class PostSynapticMechTemplate(object):

    def __init__(self, template_name=None, **kwargs):
        super(PostSynapticMechTemplate, self).__init__(**kwargs)
        self.template_name = template_name

    def instantiate(self, **kwargs):
        raise NotImplementedError()

    def get_variables(self):
        raise NotImplementedError()


class PostSynapticMechInstantiation(PostSynapticMech):
    pass



