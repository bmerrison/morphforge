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
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData, MHOCSections
from morphforgecontrib.simulation.synapses.core.postsynaptic_mechanisms import PostSynapticMech_ExpSyn
#from morphforgecontrib.stdimports import PostSynapticMech_ExpSyn
#PostSynapticMech_ExpSyn
from Cheetah.Template import Template
from morphforge.simulation.neuron.networks import NeuronSynapse
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_CurrentRecord
from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_ConductanceRecord




class Neuron_PSM_ExpSyn_CurrentRecord(Neuron_PSM_Std_CurrentRecord):
    pass

class Neuron_PSM_ExpSyn_ConductanceRecord(Neuron_PSM_Std_ConductanceRecord):
    pass

class Neuron_PSM_Exp2Syn_ConductanceRecord(Neuron_PSM_Std_ConductanceRecord):
    pass









expTmpl = """
// Post-Synapse [ $synnamepost ]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new ExpSyn ( $sectionpos )
${synnamepost}.tau = $tau.rescale("ms").magnitude
${synnamepost}.e = $eRev.rescale("mV").magnitude
"""








class Neuron_PSM_ExpSyn(PostSynapticMech_ExpSyn):

    def __init__(self, **kwargs):
        super( Neuron_PSM_ExpSyn, self).__init__(**kwargs)


    def build_hoc(self, hocFileObj):
        cell = self.celllocation.cell
        section = self.celllocation.morphlocation.section
        synNamePost = self.synapse.get_name() + "Post"
        data = {
               "synnamepost":synNamePost,
               "cell":cell,
               "cellname":hocFileObj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocFileObj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.celllocation.morphlocation.sectionpos,

               "tau": self.tau,
               "eRev": self.eRev,
               }

        hocFileObj.add_to_section( MHOCSections.InitSynapsesChemPost,  Template(expTmpl, data).respond() )

        hocFileObj[MHocFileData.Synapses][self.synapse] = {}
        hocFileObj[MHocFileData.Synapses][self.synapse]["POST"] = data

    def build_mod(self, modfile_set):
        pass


    def get_recordable(self, what, **kwargs):

        if what == NeuronSynapse.Recordables.SynapticCurrent:
            return Neuron_PSM_ExpSyn_CurrentRecord( neuron_syn_post=self, **kwargs)
        if what == NeuronSynapse.Recordables.SynapticConductance:
            return Neuron_PSM_ExpSyn_ConductanceRecord( neuron_syn_post=self, **kwargs)
        assert False


#NeuronSimulationEnvironment.registerPostSynapticMechanism( PostSynapticMech_ExpSyn, Neuron_PSM_ExpSyn)
NeuronSimulationEnvironment.postsynapticmechanisms.register_plugin(PostSynapticMech_ExpSyn, Neuron_PSM_ExpSyn)
