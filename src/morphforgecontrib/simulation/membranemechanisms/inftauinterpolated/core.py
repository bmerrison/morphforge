#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
#from ..membranemechanism import MembraneMechanism
from morphforge.core.quantities import  unit
from morphforge.simulation.core import MembraneMechanism
from morphforge.constants import StdRec

import numpy as np

class InfTauInterpolation(object):
    def __init__(self, V, inf, tau):


        assert len(V) == len(inf) == len(tau)
        assert (np.diff( np.array(V)) > 0).all()
        self.V = V
        self.inf = inf
        self.tau = tau

    def get_v_inf_vals_list(self):
        x =zip( self.V, self.inf)
        print 'getInfValsList()', x
        return x

    def get_v_tau_vals_list(self):
        return zip( self.V, self.tau)




class MM_InfTauInterpolatedChannel(MembraneMechanism):

    class Recordables():
        ConductanceDensity = StdRec.ConductanceDensity
        CurrentDensity = StdRec.CurrentDensity
        StateVar = StdRec.StateVariable
        StateVarSteadyState = StdRec.StateVarSteadyState
        StateVarTimeConstant = StdRec.StateVarTimeConstant
        all = [ConductanceDensity,CurrentDensity,StateVar,StateVarSteadyState,StateVarTimeConstant]


    def __init__(self, name, ion, equation, conductance, reversalpotential, mechanism_id, statevars_new={}):
        MembraneMechanism.__init__(self, mechanism_id=mechanism_id)
        self.name = name
        self.ion = ion
        self.eqn = equation
        self.conductance = unit(conductance)
        self.reversalpotential = unit(reversalpotential)
        self.statevars_new = statevars_new



    def get_variables(self):
        return ['gBar', 'eRev', 'gScale']

    def get_defaults(self):
        return {"gBar":self.conductance, "eRev":self.reversalpotential, "gScale": unit("1.0") }




