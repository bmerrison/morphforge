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
#from morphforge.simulation.core.networks.postsynaptic import PostSynapticMech
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData,\
    MHOCSections
from Cheetah.Template import Template
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold, PreSynapticMech_TimeList

    



    

preTmpl = """
// Pre-Synapse [ $synname ]
objref $synnamepre
${cellname}.internalsections[$sectionindex] $synnamepre = new NetCon( &v($sectionpos), $synnamepost, $threshold.rescale("mV").magnitude, $delay.rescale("ms").magnitude, $weight.rescale("uS").magnitude  )
"""

class NeuronSynapseTriggerVoltageThreshold(PreSynapticMech_VoltageThreshold):

        
    def buildHOC(self, hocFileObj):
        cell =self.celllocation.cell
        section = self.celllocation.morphlocation.section
        synName = self.synapse.getName()
        synNamePost = hocFileObj[MHocFileData.Synapses][self.synapse]["POST"]["synnamepost"]
        synNamePre = self.synapse.getName() + "Pre"
        
        
        data = {
               "synname": synName,
               "synnamepost" : synNamePost,
               "synnamepre": synNamePre,
               "cell":cell,
               "cellname":hocFileObj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocFileObj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.celllocation.morphlocation.sectionpos,
               
               "threshold": self.voltageThreshold ,
               "delay": self.delay,
               "weight": self.weight,
               }
         
        hocFileObj.addToSection( MHOCSections.InitSynapsesChemPre,  Template(preTmpl, data).respond() )
        
        hocFileObj[MHocFileData.Synapses][self.synapse]["PRE"] = data
        
        
    def buildMOD(self, modFileSet):
        pass
    
    
    
    







preTmplList = """
// Pre-Synapse [ $synname ]
objref ${synnamepre}_NullObj
objref $synnamepre
$synnamepre = new NetCon( ${synnamepre}_NullObj, $synnamepost, 0, 0, $weight.rescale("uS").magnitude  )


objref fih_${synnamepre}
fih_${synnamepre} = new FInitializeHandler("loadqueue_${synnamepre}()")
proc loadqueue_${synnamepre}() { 
#for $event in $timelist:
${synnamepre}.event( $event.getTime.rescale("ms").magnitude ) 
#end for
}


"""

class NeuronSynapseTriggerTimeList(PreSynapticMech_TimeList):
           
    def buildHOC(self, hocFileObj):
        synName = self.synapse.getName()
        synNamePost = hocFileObj[MHocFileData.Synapses][self.synapse]["POST"]["synnamepost"]
        synNamePre = self.synapse.getName() + "Pre"
        
        data = {
               "synname": synName,
               "synnamepost" : synNamePost,
               "synnamepre": synNamePre,
               "timelist": self.timeList,
               "weight": self.weight,
               }
         
        hocFileObj.addToSection( MHOCSections.InitSynapsesChemPre,  Template(preTmplList, data).respond() )
        hocFileObj[MHocFileData.Synapses][self.synapse]["PRE"] = data
        
        
    def buildMOD(self, modFileSet):
        pass 
    

#NeuronSimulationEnvironment.registerPreSynapticMechanism( PreSynapticMech_VoltageThreshold, NeuronSynapseTriggerVoltageThreshold)
#NeuronSimulationEnvironment.registerPreSynapticMechanism( PreSynapticMech_TimeList, NeuronSynapseTriggerTimeList)

NeuronSimulationEnvironment.presynapticmechanisms.registerPlugin(PreSynapticMech_VoltageThreshold, NeuronSynapseTriggerVoltageThreshold)
NeuronSimulationEnvironment.presynapticmechanisms.registerPlugin(PreSynapticMech_TimeList, NeuronSynapseTriggerTimeList)

    