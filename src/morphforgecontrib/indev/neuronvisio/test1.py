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
from morphforge.stdimports import *
from modelling.rbmodelling2 import *
from signalanalysis.stdimports import *
from neuroml_writer import MorphMLWriter


env = NeuronSimulationEnvironment()  
sim = env.Simulation()


morph = MorphologyBuilder.getSomaAxonMorph(axonLength=3000.0, axonRad=0.3, somaRad=9.0, axonSections=20)
segmenter = DefaultCellSegementer(cell=None, maxSegmentLength=50)
cell = sim.createCell(name='CellMorph1', morphology=morph, segmenter=segmenter )


t, naming_info = MorphMLWriter.writemany([cell])



print t





cell.chls = {} 
channeltypes = [ ChlType.Kf, ChlType.Ks, ChlType.Lk, ChlType.Na ]
for chltype in channeltypes:
    #mechBuilder =  ChannelLibrary.getChannelFunctor(modelsrc=Model.Sautois07, celltype=CellType.dIN, channeltype=chltype )
    mech =  ChannelLibrary.getChannel(modelsrc=Model.Sautois07, celltype=CellType.dIN, channeltype=chltype, env=env )
    
    shortcuts.ApplyMechanismEverywhereUniform(
                            cell=cell, 
                            mechanism= mech, 
                            parameter_multipliers={}, 
                            parameter_overrides={})
       
    cell.chls[chltype] = mech  


shortcuts.ApplyPassiveEverywhereUniform(cell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
shortcuts.ApplyPassiveEverywhereUniform(cell, PassiveProperty.AxialResistance, unit('40:ohmcm') )




somaLoc = cell.getLocation("soma")
sim.record( cell, name="SomaVoltage", location=somaLoc, what=Cell.Recordables.MembraneVoltage, description="Soma Voltage" ) 

distances = range(50, 3000, 100)
morph_locs = MorphLocator.getLocationsAtDistancesAwayFromSoma(morphology=morph, distances= distances )
locations = [ CellLocation(cell=cell, morphlocation=ml) for ml in morph_locs ]





print len(distances), len(morph_locs )

for loc in locations:
    sim.record( cell, location=loc, what=Cell.Recordables.MembraneVoltage, description="Distance Recording" ) 
    
    
cc = sim.createCurrentClamp( name="cclamp", amp='250:pA', dur="4:ms", delay="100:ms", celllocation=somaLoc)



# RecordAll
rec_dict = {}
for cell in sim.getCells():
    rec_dict[cell] = {}
    for seg in cell.getSegmenter():
        rec_dict[cell][seg] = {}
        
         
        rec = sim.record( cell, location=seg.getCellLocation(), what=Cell.Recordables.MembraneVoltage )
        rec_dict[cell][seg]['V'] = rec.name
         
        print rec


#assert False




res = sim.Run()





#Build the HDF5 file:


import tables
import os
fName ="/home/michael/Desktop/test1.hdf5"

if os.path.exists(fName):
    os.unlink(fName)
    
h5file = tables.openFile(fName, mode = "w", title = "Test file")  

geom = h5file.createGroup("/", 'geometry', )
#geom. = h5file.createGroup(geom, 'geom', )

h5file.createArray(geom, 'geom', str(t) )

results = h5file.createGroup("/", 'results', )
varref = h5file.createGroup(results , 'VarRef', )
    

time = None


for cell,segs in rec_dict.iteritems():
    for seg,vars in segs.iteritems():
        
        seg_names,seg_ids = naming_info[cell]
        
        seg_name = seg_names[seg]
        segGrp = h5file.createGroup(varref, seg_name )
        
        for var,varname in vars.iteritems():
            tr = res.getTrace( varname )
            h5file.createArray(segGrp,  var, tr._data.magnitude )
            
            if time is None:
                time = tr._time.rescale("ms").magnitude
            
h5file.createArray(varref,  "x", time )


h5file.close()


TagViewer(res, show=False)


#    pylab.show()