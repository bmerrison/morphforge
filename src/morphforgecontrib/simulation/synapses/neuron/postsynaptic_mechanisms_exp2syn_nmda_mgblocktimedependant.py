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
from morphforgecontrib.simulation.synapses.core import PostSynapticMech_Exp2SynNMDA
from Cheetah.Template import Template
from morphforge.simulation.neuron.networks import NeuronSynapse, Synapse
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment


from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_CurrentRecord
from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_ConductanceRecord
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.core.mfrandom import MFRandom
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.synapses.neuron import postsynaptic_mechanisms_exp2syn_nmda_mgblocktimedep_modfile



class Neuron_PSM_Exp2SynNMDA_CurrentRecord(Neuron_PSM_Std_CurrentRecord):
    pass


class Neuron_PSM_Exp2SynNMDA_ConductanceRecord(Neuron_PSM_Std_ConductanceRecord):
    pass


class Neuron_PSM_Std_NMDAVoltageDependanceRecord(NeuronRecordable):

    def __init__(self, neuron_syn_post, **kwargs):
        super(Neuron_PSM_Std_NMDAVoltageDependanceRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def getUnit(self):
        return unit("")
    def getStdTags(self):
        return [StandardTags.NMDAVoltageDependancy]

    def buildHOC(self, hocFile):
        objNameHoc = hocFile[MHocFileData.Synapses][self.neuron_syn_post.synapse]["POST"]["synnamepost"]
        HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="voltage_dep_state", recordobj=self )
                
    def buildMOD(self, modFileSet):
        pass    
    
    
class Neuron_PSM_Std_NMDAVoltageDependanceSteddyStateRecord(NeuronRecordable):

    def __init__(self, neuron_syn_post, **kwargs):
        super(Neuron_PSM_Std_NMDAVoltageDependanceSteddyStateRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def getUnit(self):
        return unit("")
    def getStdTags(self):
        return [StandardTags.NMDAVoltageDependancySS]

    def buildHOC(self, hocFile):
        objNameHoc = hocFile[MHocFileData.Synapses][self.neuron_syn_post.synapse]["POST"]["synnamepost"]
        HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="voltage_dependancy_ss", recordobj=self )
                
    def buildMOD(self, modFileSet):
        pass        
    




exp2HOCTmpl = """
// Post-Synapse [ $synnamepost ]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new Exp2SynNMDATimeDepBlockMorphforge ( $sectionpos )
${synnamepost}.tau1 = $tauOpen.rescale("ms").magnitude
${synnamepost}.tau2 = $tauClosed.rescale("ms").magnitude
${synnamepost}.e = $eRev.rescale("mV").magnitude
${synnamepost}.popening = $pOpening

"""

class PostSynapticMech_Exp2SynNMDAMGTimeDepBlock( PostSynapticMech_Exp2SynNMDA ):
    pass

class Neuron_PSM_Exp2SynNMDAMgBlockTimeDep(PostSynapticMech_Exp2SynNMDAMGTimeDepBlock):   
    
   
    def __init__(self, simulation, **kwargs):
        PostSynapticMech_Exp2SynNMDA.__init__( self,  **kwargs)
        
        


    def buildHOC(self, hocFileObj):
        cell = self.celllocation.cell
        section = self.celllocation.morphlocation.section
        synNamePost = self.synapse.getName() + "Post"
        data = {
               "synnamepost":synNamePost,
               "cell":cell,
               "cellname":hocFileObj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocFileObj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.celllocation.morphlocation.sectionpos,
               
               "tauOpen": self.tauOpen,
               "tauClosed": self.tauClosed,
               "eRev": self.eRev,
               "pOpening": self.popening,
               'random_seed': MFRandom.getSeed(),
               }
        
        hocFileObj.addToSection( MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond() )
        
        hocFileObj[MHocFileData.Synapses][self.synapse] = {}
        hocFileObj[MHocFileData.Synapses][self.synapse]["POST"] = data  
        
    def buildMOD(self, modFileSet):
        #import postsynaptic_mechanisms_exp2syn_nmda_modfile
        modfile = ModFile(modtxt=postsynaptic_mechanisms_exp2syn_nmda_mgblocktimedep_modfile.getExp2SynNMDAMgBlockTimeDependanceModfile(), name='UnusedParameterXXXExpSyn2')
        modFileSet.append(modfile)
        
        
        
    def getRecordable(self, what, **kwargs):
        if what == Synapse.Recordables.SynapticCurrent:
            return Neuron_PSM_Exp2SynNMDA_CurrentRecord( neuron_syn_post=self, **kwargs)
        if what == Synapse.Recordables.SynapticConductance:
            return Neuron_PSM_Exp2SynNMDA_ConductanceRecord( neuron_syn_post=self, **kwargs)
        if what == StandardTags.NMDAVoltageDependancy:
            return Neuron_PSM_Std_NMDAVoltageDependanceRecord( neuron_syn_post=self, **kwargs)
        if what == StandardTags.NMDAVoltageDependancySS:
            return Neuron_PSM_Std_NMDAVoltageDependanceSteddyStateRecord( neuron_syn_post=self, **kwargs)
        
        assert False
        
        
        
        
NeuronSimulationEnvironment.postsynapticmechanisms.registerPlugin(PostSynapticMech_Exp2SynNMDAMGTimeDepBlock, Neuron_PSM_Exp2SynNMDAMgBlockTimeDep)
