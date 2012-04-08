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

"""Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface.
We look at the effect of changing the density of leak and sodium channels in just the axon 
of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and 
then tell the TagViewer to plot everything with a tag 'SIMY' 

"""



from morphforge.stdimports import *
from morphforgecontrib.data_library.stdmodels import StandardModels


def sim( glk_multiplier, gna_multiplier, tag):
    # Create the environment:
    env = NeuronSimulationEnvironment()
    
    # Create the simulation:
    mySim = env.Simulation()
    
    # Create a cell:
    morph = MorphologyBuilder.getSomaAxonMorph(axonLength=3000.0, axonRad=0.3, somaRad=9.0, axonSections=20)
    myCell = mySim.createCell(name="Cell1", morphology=morph)
    
    
    lkChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    naChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Na", env=env) 
    kChannels  = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="K", env=env) 
     
    # Apply the channels uniformly over the cell
    ApplyMechanismEverywhereUniform(myCell, lkChannels )
    ApplyMechanismEverywhereUniform(myCell, naChannels )
    ApplyMechanismEverywhereUniform(myCell, kChannels )
    
    # Over-ride the parameters in the axon:
    ApplyMechanismRegionUniform(cell=myCell, mechanism=lkChannels, region=morph.getRegion("axon"), parameter_multipliers={'gScale':glk_multiplier})
    ApplyMechanismRegionUniform(cell=myCell, mechanism=naChannels, region=morph.getRegion("axon"), parameter_multipliers={'gScale':gna_multiplier})
    
    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
    
    
    for cell_location in CellLocator.getLocationsAtDistancesAwayFromDummy(cell=myCell, distances=range(9, 3000, 100) ):
        mySim.record( myCell, what=StdRec.MembraneVoltage, location=cell_location, user_tags=[tag])
    
    # Create the stimulus and record the injected current:
    cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), celllocation=myCell.getLocation("soma"))
    mySim.record( cc, what=StdRec.Current)
    
    # Run the simulation
    return mySim.Run()
    

# Display the results:
results_a = [     
    sim( glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
    sim( glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
    sim( glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
    sim( glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
    sim( glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
]

TagViewer(results_a, timeranges=[(97.5, 140)*pq.ms], show=False,
          plotspecs = [
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),  
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                        ] )

results_b = [
    sim( gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),     
    sim( gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
    sim( gna_multiplier=0.75,  glk_multiplier=1.0, tag="SIM8"),
    sim( gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
]

TagViewer(results_b, timeranges=[(97.5, 140)*pq.ms],show=True,
          plotspecs = [
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),  
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
                        ] )

