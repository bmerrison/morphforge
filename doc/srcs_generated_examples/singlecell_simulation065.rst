
15. Using a channel library to reduce duplication
=================================================


Using a channel library to reduce duplication.

We define functions that produce morphology and channel objects for our simulations.
We could stop here, and simply import and use the functions in our simulations, but
we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
These are basically glorified dictionaries, that do the lookup for the appropriate functors
based on a key from the tuple~(modelsrc, celltype, channeltype). The advantage for doing this is that
there is single repository for morphologies and channels.

There is not really anythin clever going on here, and you can run simulations completely ignorantly
of these classes, I just included it because it made life much easier for me, when I had to start managing
lots of channel definitions.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	
	# This can be put into a file that is loaded on
	# you path somewhere:
	
	# ======================================================
	def getSimpleMorphology():
	
	    mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma',   } }
	    return  MorphologyTree.fromDictionary(mDict)
	
	
	def get_sample_lk(env):
	    lkChannels = env.MembraneMechanism(
	                         MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("0.3:mS/cm2"),
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	    return lkChannels
	
	
	def get_sample_na(env):
	    naStateVars = { "m": {
	                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
	                          "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
	                        "h": {
	                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
	                            "beta": [1.00,0.00,1.00,35.00,-10.00]}
	                      }
	
	    naChannels = env.MembraneMechanism(
	                            MM_AlphaBetaChannel,
	                            name="NaChl", ion="na",
	                            equation="m*m*m*h",
	                            conductance=unit("120:mS/cm2"),
	                            reversalpotential=unit("50:mV"),
	                            statevars=naStateVars,
	                            mechanism_id="HH_NA_CURRENT"
	                            )
	    return naChannels
	
	
	def get_sample_k(env):
	    kStateVars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
	                          "beta": [0.125,0,0,65,80]},
	                       }
	    kChannels = env.MembraneMechanism(
	                            MM_AlphaBetaChannel,
	                            name="KChl", ion="k",
	                            equation="n*n*n*n",
	                            conductance=unit("36:mS/cm2"),
	                            reversalpotential=unit("-77:mV"),
	                            statevars=kStateVars,
	                            mechanism_id="HH_K_CURRENT"
	                            )
	    return kChannels
	
	
	
	MorphologyLibrary.register_morphology(modelsrc="Sample", celltype="Cell1", morph_functor=getSimpleMorphology)
	ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Na", chl_functor=get_sample_na)
	ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="K", chl_functor=get_sample_k)
	ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Lk", chl_functor=get_sample_lk)
	
	# =============================================================
	
	
	
	
	
	
	
	
	
	# Now in our script elsewhere, we can use them as:
	modelsrc = "Sample"
	celltype="Cell1"
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	# Create a cell:
	morphology=MorphologyLibrary.get_morphology(modelsrc=modelsrc, celltype=celltype)
	myCell = mySim.create_cell(morphology=morphology )
	
	# Apply the channels uniformly over the cell
	naChls = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Na", env=env)
	kChls  = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="K", env=env)
	lkChls = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Lk", env=env)
	
	apply_mechanism_everywhere_uniform(myCell, naChls )
	apply_mechanism_everywhere_uniform(myCell, kChls  )
	apply_mechanism_everywhere_uniform(myCell, lkChls )
	
	apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a cell_location on the cell:
	somaLoc = myCell.get_location("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.create_currentclamp( name="Stim1", amp=unit("150:pA"), dur=unit("5:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	
	mySim.record( cc, what=StandardTags.Current)
	mySim.record( myCell, what=StandardTags.Voltage, cell_location=somaLoc )
	
	
	# run the simulation
	results = mySim.run()
	
	# Display the results:
	TagViewer([results], timeranges=[(97.5, 140)*pq.ms] )
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation065_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation065_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:21:45,580 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:45,580 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xaf1716c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xaf202ec>
	Saving File _output/figures/singlecell_simulation065/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation065/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation065/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation065/svg/fig000_Autosave_figure_1.svg
	




