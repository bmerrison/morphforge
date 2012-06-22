#!/usr/bin/env python
from __future__ import division


from chaco.api import Plot, ArrayPlotData, add_default_axes, add_default_grids, OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot
from chaco.example_support import COLOR_PALETTE
from chaco.tools.api import PanTool, ZoomTool, BroadcasterTool
from modelling.rbmodelling2.modelconstants import ChlType, Model, CellType
from morphforge.stdimports import * 

from traitsui.api import View, Item, Group, Tabbed
from enable.component_editor import ComponentEditor
from traits.has_traits import HasTraits, on_trait_change
from traits.trait_types import Instance, Range
from morphforgecontrib.simulation.membranemechanisms.inftauinterpolated.core import MM_InfTauInterpolatedChannel
from channel_panels import HHChannelPaneInfTau1,\
    HHChannelExistingChannel, HHChannelPaneLk, buildPaneFromExistingChannel,\
    buildPaneFromExistingChannelLk
from chaco_util import HGroup, VGroup
from channel_panels import buildPaneFromExistingChannelInfTau1State
from channel_panels import HHChannelPaneInfTau2,buildPaneFromExistingChannelInfTau2State












vUnit = 'mV'
iUnit = 'pA/um2'
gUnit = 'pS/um2'
trace_names = [ ('SomaVoltage',vUnit), 
                ('Kf_i',iUnit), ('Ks_i',iUnit),('Lk_i',iUnit),('Na_i',iUnit), ('Ca_i', iUnit), 
                ('Kf_g',gUnit), ('Ks_g',gUnit),('Lk_g',gUnit),('Na_g',gUnit),
                ('Ks_ks',''), ('Kf_kf',''), ('Na_m',''),('Na_h',''),
                ]


trace_names = [ ('SomaVoltage',vUnit), ]








class TracePlot(HasTraits):
    
    plot = Instance(Plot)
    view = View(
            Group(
                  Item('plot',editor=ComponentEditor(size=(50,50)),show_label=False),
                ),
                resizable=True) 
    
    def __init__(self, sim_conf, plot_what, colors, xRange=None, yRange=None):
        super(TracePlot, self).__init__()
        
        sim_conf.add_simulation_display_functor( self.update_display )

        self.plot = Plot(sim_conf.data,resizable='v')
        self.plot.padding =25
        self.plot.fill_padding=True



        # Setup the axis:
        if xRange:
            self.plot.x_mapper.range.set_bounds(*xRange)
        if yRange:
            self.plot.y_mapper.range.set_bounds(*yRange)

        for what,color in zip( plot_what,colors ):
            render = self.plot.plot((what+"_t",what + "_d"),type='line' ,color=color)

        
        broadcaster = BroadcasterTool()
        broadcaster.tools.append(PanTool(self.plot))
        zoom = ZoomTool(component=self.plot, tool_mode="box", always_on=False,pointer = 'magnifier', border_color='black', border_size=3, alpha=0.5,  color='lightskyblue')
        broadcaster.tools.append(zoom)
        self.plot.tools.append(broadcaster)


    def update_display(self):
        pass        



#class SimulationRunWindow(HasTraits):



class SimulationConfig(HasTraits):

    data = Instance( ArrayPlotData)


    def __init__(self):
        super(SimulationConfig, self).__init__()


        self.x = np.linspace(0,100,1000)
        y1 = np.sin(self.x)

        rec_dict = {}
        for tn, tunit in trace_names:
            rec_dict[tn+'_t'] = self.x
            rec_dict[tn+'_d'] = y1

        #self.data = ArrayPlotData(SomaVoltage_t=self.x,SomaVoltage_d=y1,y2=y2)
        self.data = ArrayPlotData(**rec_dict)

        self.cell_builder_func = None
        self.input_stimulus_builder = None
        self.simulation_chl_functors = []
        self.display_functors = []


    def add_simulation_chl_functor(self, simulation_chl_functor):
        self.simulation_chl_functors.append( simulation_chl_functor)


    def add_simulation_display_functor(self, display_functor):
        self.display_functors.append( display_functor)


        

    def resimulate(self):


        # Get the cell size, the input stimulus


        env = NeuronSimulationEnvironment()
        sim = env.Simulation()

        cell = self.cell_builder_func(env=env, sim=sim)
        self.input_stimulus_builder(sim=sim, cell=cell)




        #caFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Ca)
        #caChl = caFunctor(env)
        #shortcuts.apply_mechanism_everywhere_uniform(cell=cell, mechanism=caChl)



        mech_dict = {}
        # Apply the channels:
        for chl in self.simulation_chl_functors:
            mech = chl.getMechanism(env=env)
            mech_dict[chl.chlname] = mech
            if mech:
                # Apply the mechanism:
                apply_mechanism_everywhere_uniform(cell=cell, mechanism=mech)



        #Record the Currents & Conductances:
        for chlname, mech in mech_dict.iteritems():
                sim.record( mech,  what = StdRec.CurrentDensity, where=cell.getLocation('soma'), name="%s_i"%chlname, description="")
                if chlname != 'Ca':
                    sim.record( mech,  what = StdRec.ConductanceDensity, where=cell.getLocation('soma'), name="%s_g"%chlname, description="")

       
        
        
        sim.record( mech_dict['Kf'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='kf',  name="Kf_kf",  where = cell.getLocation('soma'), description='Kf State')
        sim.record( mech_dict['Ks'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='ks',  name="Ks_ks",  where = cell.getLocation('soma'), description='Ks State')
        sim.record( mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='m',  name="Na_m",  where = cell.getLocation('soma'), description='Na-m State')
        sim.record( mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='h',  name="Na_h",  where = cell.getLocation('soma'), description='Na-h State')
    
        # Record Voltages:
        sim.record( cell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = cell.getLocation('soma'), description='Membrane Voltage')





        res = sim.Run()

            
        # Update the array of data:
        for trace_name, trace_unit in trace_names:
            tr = res.getTrace(trace_name)
            self.data.set_data(trace_name+'_t', tr._time.rescale('ms').magnitude )
            self.data.set_data(trace_name+'_d', tr._data.rescale(trace_unit).magnitude )


        # Update the display:
        for display_func in self.display_functors:
            display_func()


        print 'Done simulating'


        
        










class MorphologyConfig(HasTraits):
    surfacearea = Range(1.0, 1000., 590)
    capacitance = Range(0.1, 10.0, 1.0)
    view = View(Group(
                  Item('surfacearea',), 
                  Item('capacitance',), 
                ),
                resizable=True,title='Morphology')

    def __init__(self,sim_conf):
        super(MorphologyConfig, self).__init__()
        self.sim_conf = sim_conf
        sim_conf.cell_builder_func = self.getCell
        
        

    @on_trait_change('surfacearea, capacitance')
    def m_update(self):
        self.sim_conf.resimulate()



    def getCell(self, env, sim):
        m1 = MorphologyBuilder.getSingleSectionSoma(area= float(self.surfacearea) * um2 )
        #m1 = 
        
        morphFunctor = MorphologyLibrary.getMorphologyFunctor(modelsrc=Model.Hull12SWithAxon, celltype=CellType.dIN )
        m1 = morphFunctor(axonDiam = 0.4)
        
        myCell = sim.createCell(name="Cell1", morphology=m1)
        apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('%f:uF/cm2'%self.capacitance) )
        return myCell



class InputConfig(HasTraits):
    amp1 =      Range(-1000.0, 1000., 200)
    delay1 =    Range(0.0, 1000., 100)
    dur1 =      Range(0.0, 1000., 100)
    amp2 =      Range(-1000.0, 1000., 0)
    delay2 =    Range(0.0, 1000., 105)
    dur2 =      Range(0.0, 1000., 5)

    sim_conf = Instance( SimulationConfig )
    view = View(
            Group(
                  Item('amp1'),
                  Item('delay1'),
                  Item('dur1'),
                ),
            Group(
                  Item('amp2'),
                  Item('delay2'),
                  Item('dur2'),
                ),
                resizable=True,title='Current Inj')

    def __init__(self,sim_conf):
        super(InputConfig, self).__init__()
        self.sim_conf = sim_conf
        self.sim_conf.input_stimulus_builder = self.getInputStimulus

    @on_trait_change('amp1, amp2, dur1, dur2, delay1, delay2')
    def on_update(self):
        self.sim_conf.resimulate()

    def getInputStimulus(self, sim, cell):
        somaLoc = cell.getLocation("soma")
        s1 = sim.createCurrentClamp( name="Stim1", amp=unit("%2.2f:pA"%self.amp1), dur=unit("%f:ms"%self.dur1), delay=unit("%f:ms"%self.delay1), celllocation=somaLoc)
        s2 = sim.createCurrentClamp( name="Stim2", amp=unit("%2.2f:pA"%self.amp2), dur=unit("%f:ms"%self.dur2), delay=unit("%f:ms"%self.delay2), celllocation=somaLoc)
        return None





class Double(HasTraits):

    s3 = Instance( TracePlot )
    s4 = Instance( TracePlot )
    s5 = Instance( TracePlot )
    s6 = Instance( TracePlot )
    conf_morph= Instance( MorphologyConfig )
    conf_input = Instance( InputConfig )

    hhKf = Instance( HHChannelPaneInfTau1 )
    hhKs = Instance( HHChannelPaneInfTau1 )
    hhNa = Instance( HHChannelPaneInfTau2 )
    hhCa = Instance( HHChannelExistingChannel )
    hhLk = Instance( HHChannelPaneLk )

    view = View(
            HGroup(
             VGroup(
                 Tabbed(
                     Item('hhLk', style='custom',show_label=False),
                     Item('hhKf', style='custom',show_label=False),
                     Item('hhKs', style='custom',show_label=False),
                     Item('hhNa', style='custom',show_label=False),
                     Item('hhCa', style='custom',show_label=False),
                     )
             ),
              VGroup(
               Item('s3', style='custom', show_label=False ), 
               Item('s4', style='custom', show_label=False ), 
               Item('s5', style='custom', show_label=False ), 
               Item('s6', style='custom', show_label=False ), 
              ),
              VGroup(
               Item('conf_morph', style='custom', show_label=False ), 
               Item('conf_input', style='custom', show_label=False ), 
              ),
              ),
             
            resizable=True, width=1200, height=1200, )




#naFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.Sautois07, celltype=CellType.dIN, channeltype=ChlType.Na)
#kfFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.Sautois07, celltype=CellType.dIN, channeltype=ChlType.Kf)
#ksFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.Sautois07, celltype=CellType.dIN, channeltype=ChlType.Ks)
#
#
#naFunctorOld = ChannelLibrary.getChannelFunctor(modelsrc=Model.Hull10, celltype=CellType.RB, channeltype=ChlType.Na)
#kfFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.Hull10, celltype=CellType.RB, channeltype=ChlType.Kf)
#ksFunctor = ChannelLibrary.getChannelFunctor(modelsrc=Model.Hull10, celltype=CellType.RB, channeltype=ChlType.Ks)

#
#naFunctorBase = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Na)
#kfFunctorBase = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Kf)
#ksFunctorBase = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Ks)
#lkFunctorBase = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Lk)
#caFunctorBase = ChannelLibrary.getChannelFunctor(modelsrc=Model.BigSim6, celltype=CellType.RB, channeltype=ChlType.Ca)
##ChannelLibrary.registerChannel(modelsrc = Model.BigSim6, celltype=CellType.RB, channeltype= ChlType.Ca, chlFunctor=getCaChannels )
##ChannelLibrary.registerChannel(modelsrc = Model.BigSim6, celltype=CellType.RB, channeltype= ChlType.Kf, chlFunctor=getKfChannels )
##ChannelLibrary.registerChannel(modelsrc = Model.BigSim6, celltype=CellType.RB, channeltype= ChlType.Ks, chlFunctor=getKsChannels )
##ChannelLibrary.registerChannel(modelsrc = Model.BigSim6, celltype=CellType.RB, channeltype= ChlType.Lk, chlFunctor=getLkChannels )
##ChannelLibrary.registerChannel(modelsrc = Model.BigSim6, celltype=CellType.RB, channeltype= ChlType.Na, chlFunctor=getNaChannels )
#
##
#
#caMult = 1.0
#naMult = 1.6
#kfMult = 0.6
#ksMult = 1.0
#lkMult = 1.2
##nrnParams = NeuronParameters( { ChlIon.Na: 1.6, ChlIon.Ca: 1.0, ChlIon.Kf: 0.6, ChlIon.Lk: 1.2 } )
#
#
##nrnParams = NeuronParameters( { ChlIon.Na: 1.0, ChlIon.Ca: 1.6, ChlIon.Kf: 0.5, ChlIon.Lk: 0.4 } )




"""
        for mechFunctor in mechFunctors:
            mech = mechFunctor( env=sim.environment )
            if mechFunctor == lkFunctor:
                
                if coupled_leak:
                    apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':0.5}, parameter_overrides = {'eLk':unit("-52.0:mV")}  )
                else:
                    apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':1.0}, parameter_overrides = {'eLk':unit("-52.0:mV")}  )
                    

            elif mechFunctor == naFunctor:
                if disable_sodium:
                    continue
                
                apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':2.5} )
                apply_mechanism_region_uniform(    cell=myCell, mechanism=mech, region=myCell.morphology.getRegion('axon'), parameter_multipliers={'gScale':5.0} )
                    
                
            elif mechFunctor == kfFunctor:
                if disable_kf:
                    continue
                
                apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':0.5} )
                apply_mechanism_region_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':0.5} , region=myCell.morphology.getRegion('soma'))
                
            elif mechFunctor == ksFunctor:
                apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech, parameter_multipliers={'gScale':0.5} )
                
            else:
                apply_mechanism_everywhere_uniform(cell=myCell, mechanism=mech)
                """

caMult = 1.0
naMult = 5.0
lkMult = 1.0
ksMult = 0.5
kfMult = 2.5
lkFunctorBase = ChannelLibrary.getChannelFunctor( modelsrc=Model.Hull12, celltype=CellType.dIN, channeltype=ChlType.Lk)
caFunctorBase = ChannelLibrary.getChannelFunctor( modelsrc=Model.Hull12, celltype=CellType.dIN, channeltype=ChlType.Ca)
naFunctorBase = ChannelLibrary.getChannelFunctor( modelsrc=Model.Dale95, celltype=CellType.RB,  channeltype=ChlType.Na)
kfFunctorBase = ChannelLibrary.getChannelFunctor( modelsrc=Model.Hull12, celltype=CellType.DL,  channeltype=ChlType.Kf)
ksFunctorBase = ChannelLibrary.getChannelFunctor( modelsrc=Model.Hull12, celltype=CellType.RB,  channeltype=ChlType.Ks)

def caFunctor(env):
    chl = caFunctorBase(env)
    chl.permeability *= caMult
    return chl

def naFunctor(env):
    chl = naFunctorBase(env)
    chl.conductance *= naMult
    return chl

def kfFunctor(env):
    chl = kfFunctorBase(env)
    chl.conductance *= kfMult
    return chl

def ksFunctor(env):
    chl = ksFunctorBase(env)
    chl.conductance *= ksMult
    return chl

def lkFunctor(env):
    chl = lkFunctorBase(env)
    chl.conductance *= lkMult
    return chl







def main():

    sim_conf = SimulationConfig()
    sim_config = sim_conf
    
    xRange=(95, 130)

    d = Double(
            s3 = TracePlot(sim_conf=sim_conf, plot_what=['SomaVoltage'], colors=['green'], yRange=(-80,50),xRange=xRange),
            #s4 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_i','Ks_i','Lk_i','Na_i','Ca_i'], colors=['cyan','blue','red','green','orange'],xRange=xRange), 
            #s5 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_g','Ks_g','Lk_g','Na_g'], colors=['cyan','blue','red','green'],xRange=xRange), 
            #s6 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_kf','Ks_ks','Na_m','Na_h'], colors=['cyan','blue','red','green'],xRange=xRange), 
            conf_morph= MorphologyConfig(sim_conf=sim_conf),
            conf_input= InputConfig(sim_conf=sim_conf),

            hhKs = buildPaneFromExistingChannelInfTau1State( ksFunctor, sim_config=sim_config, chlname='Ks' ) ,
            hhKf = buildPaneFromExistingChannelInfTau1State( kfFunctor, sim_config=sim_config, chlname='Kf' ) ,
            hhNa = buildPaneFromExistingChannelInfTau2State( naFunctor, sim_config=sim_config, chlname='Na' ) ,
            hhCa = buildPaneFromExistingChannel( caFunctor, sim_config=sim_config,chlname='Ca' ) ,
            hhLk = buildPaneFromExistingChannelLk(lkFunctor, sim_config=sim_config, chlname='Lk' ) ,
            )
    d.configure_traits()


#vrev=unit('-54:mV'), gbar=unit('0.5:mS/cm2')

if __name__ == '__main__':
    main()

































