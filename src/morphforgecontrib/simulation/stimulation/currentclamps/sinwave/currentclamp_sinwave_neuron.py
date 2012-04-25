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
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData,\
    MHOCSections
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.stimulation.currentclamps.sinwave.currentclamp_sinwave_core import CurrentClamp_SinWave
from morphforge.simulation.neuron.objects.neuronobject import NeuronObject
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from Cheetah.Template import Template



currentclampsinwaveTxt = """
COMMENT
TODO: ATTRIBUTION.
ENDCOMMENT


NEURON {
        POINT_PROCESS CurrentClampSinWave
        RANGE del, dur, pkamp, freq, phase, bias
        ELECTRODE_CURRENT i
}

UNITS {
        (nA) = (nanoamp)
             }

PARAMETER {
        del=5   (ms)
        dur=1000   (ms)
        pkamp=10 (nA)
        freq=10  (Hz)
        phase=0 (rad)
        bias=0  (nA)
        PI=3.14159265358979323846
}

ASSIGNED {
        i (nA)
}

BREAKPOINT {
    at_time(del)
    at_time(del + dur)
    
    if (t < del) {
          i=0   
       }else{  
                if (t < del+dur) {
               i = pkamp*sin(2*PI*freq*(t-del)/1000+phase)+bias
          }else{  
               i = 0
}}}
"""




ccSinWaveHOCTmpl = """
// Post-Synapse [ $stimname ]
objref $stimname
${cellname}.internalsections[$sectionindex] $stimname = new CurrentClampSinWave ( $sectionpos )
${stimname}.freq =     $freq.rescale("Hz").magnitude
${stimname}.pkamp =      $amp.rescale("nA").magnitude
${stimname}.del =    $delay.rescale("ms").magnitude
${stimname}.bias = $bias.rescale("nA").magnitude

"""




class NeuronSinwaveCurrentClampCurrentRecord(NeuronRecordable):
    def __init__(self, cclamp, **kwargs):
        super(NeuronSinwaveCurrentClampCurrentRecord,self).__init__(**kwargs)
        self.cclamp = cclamp    

    def getUnit(self):
        return unit("nA")
    def getStdTags(self):
        return [StandardTags.Current]


    def buildHOC(self, hocFile):
        objNameHoc = hocFile[MHocFileData.CurrentClamps][self.cclamp]["stimname"]
        HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, name=objNameHoc, objvar="i", recordobj=self )

    def buildMOD(self, modFileSet):
        pass





        
        
class Neuron_CurrentClamp_SinWave(CurrentClamp_SinWave, NeuronObject):
    
    def __init__(self, simulation,  amp, freq, delay,bias, celllocation, name):
        assert False, "Resolve the multiple inheritance of the name!"
        
        NeuronObject.__init__(self, simulation=simulation, name=name)
        CurrentClamp_SinWave.__init__(self,  amp=amp, freq=freq, delay=delay, bias=bias, celllocation=celllocation, name=name )
                

    def buildHOC(self, hocFileObj):
        cell = self.celllocation.cell
        section = self.celllocation.morphlocation.section
        
        data = {
               "stimname": self.getName(),
               "cell":cell,
               "cellname":hocFileObj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocFileObj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.celllocation.morphlocation.sectionpos,
               
               "freq": self.freq,
               "amp": self.amp,
               "delay": self.delay,
               "bias":self.bias,
               }
        
        hocFileObj.addToSection( MHOCSections.InitCurrentClamps,  Template(ccSinWaveHOCTmpl, data).respond() )
        
        hocFileObj[MHocFileData.CurrentClamps][self] = data
          
        
    def buildMOD(self, modFileSet):
        modfile = ModFile(modtxt=currentclampsinwaveTxt, name='NeuronSinWaveCurrentClmap')
        modFileSet.append(modfile)
        
        
        
    def getRecordable(self, what, **kwargs):
        if what == StandardTags.Current:
            return NeuronSinwaveCurrentClampCurrentRecord( cclamp=self, **kwargs)
        assert False
    
    
        

        

#NeuronSimulationEnvironment.registerMembraneMechanism( CurrentClamp_SinWave, Neuron_CurrentClamp_SinWave)