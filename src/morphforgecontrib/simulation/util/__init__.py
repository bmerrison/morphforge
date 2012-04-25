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
from voltageclampchannel import getVCSomaCurrentTrace
from calculate_input_resistance import CellAnalysis_IVCurve, CellAnalysis_ReboundResponse, CellAnalysis_StepInputResponse

import numpy as np
from morphforge.core.misc import FilterExpectSingle


def execWithProb(p, func):
    def new_func(*args,**kwargs):
        if np.random.sample() < p:
            return func(*args,**kwargs)
        else:
            return None
    return new_func




def record_from_mechanism( sim, mechanism_name, where, what, on_error_skip=False, user_tags = None, **kwargs ):
    user_tags = user_tags or []
     
    assert on_error_skip==False
     
    
    mechs = where.cell.getBiophysics().getAllMechanismsAppliedToCell()
    
    recs = []
    
    mech = FilterExpectSingle( seq=mechs, filterFunc= lambda m:m.name==mechanism_name)
    r = sim.record( mech, what=what, where = where, user_tags = user_tags + [mech.name], **kwargs )
    
    return r
    #for mech in mechs:
    #    if mech.na
        #print "Recording:", mech
        
   #     recs.append(r)
        
    #return recs



def record_from_all_mechanisms( sim, where, what, on_error_skip=False, user_tags = None, **kwargs ):
    user_tags = user_tags or []
     
    assert on_error_skip==False
     
    cell = where.cell
    
    mechs = cell.getBiophysics().getAllMechanismsAppliedToCell()
    
    recs = []
    for mech in mechs:
        #print "Recording:", mech
        r = sim.record( mech, what=what, where = where, user_tags = user_tags + [mech.name], **kwargs )
        recs.append(r)
        
    return recs