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
from morphology.util import AxonTrimmer
from morphology.util import CellLocationDistanceFromSoma
from morphology.util import MorphologyTranslator 


# Simulation Channels:
from simulation.membranemechanisms.inftauinterpolated.core import MM_InfTauInterpolatedChannel, InfTauInterpolation
from simulation.membranemechanisms.hh_style.core import MM_AlphaBetaChannel, MM_LeakChannel, MM_AlphaBetaBetaChannel    
from simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel



from morphforgecontrib.simulation.util.voltageclampchannel import getVCSomaCurrentTrace
from morphforgecontrib.simulation.util.calculate_input_resistance import CellAnalysis_IVCurve

from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_TimeList,\
    PreSynapticMech_VoltageThreshold
from morphforgecontrib.simulation.synapses.core.postsynaptic_mechanisms import PostSynapticMech_Exp2Syn,\
    PostSynapticMech_ExpSyn,PostSynapticMech_Exp2SynNMDA

from morphforgecontrib.simulation.synapses.neuron.postsynaptic_mechanisms_exp2syn_nmda_mgblocktimedependant import PostSynapticMech_Exp2SynNMDAMGTimeDepBlock


#Traces:
from traces import AutoTaggerFromUnit


from morphforgecontrib.simulation.populations import NeuronPopulation, Connectors, PopAnalSpiking, SynapsePopulation
from morphforgecontrib.traces.tracetools import SpikeFinder


from morphforgecontrib.simulation.util.calculate_input_resistance import CellAnalysis_IVCurve, CellAnalysis_StepInputResponse, CellAnalysis_ReboundResponse

from morphforgecontrib.simulation.util.spaced_recordings import SpaceRecordCell
from morphforgecontrib.simulation.util import execWithProb 
from morphforgecontrib.simulation.synapse_management.util import SynapseParameter, create_synapse_cell_to_cell, create_synapse_times_to_cell



from morphforgecontrib.tags import StdTagFunctors, UserTagFunctorCellLocation#, UserTagFunctorNeuronPopulation


from morphforgecontrib.simulation_analysis.spikinggrouping import DBScan

# Mike Hull development:
from socket import gethostname
if gethostname() in ["michael-DQ57TM"]:
    
    from morphforgecontrib.mhdev import *

