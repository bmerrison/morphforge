#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

from morphforge.core import is_iterable
from morphforge.core import unit
from morphforge.simulation.base import SimulationResult
from morphforge.core.quantities import mV, ms, Quantity
from mhlibs.quantities_plot import QuantitiesFigure
from plotspecs import TagPlot
from morphforge.traces import TraceFixedDT
from morphforge.traces import TraceVariableDT
from morphforge.traces import TracePiecewise
from morphforge.traces.eventset import EventSet
from morphforge.core import quantities as pq

# pylint: disable=W0108
# (Suppress warning about 'unnessesary lambda functions')



class DefaultTagPlots(object):
    Voltage =            TagPlot("Voltage", ylabel='Voltage', yrange=(-80*mV, 50*mV), yunit=pq.millivolt )
    CurrentDensity =     TagPlot("CurrentDensity", ylabel='CurrentDensity', yunit=pq.milliamp / pq.cm2 )
    Current =            TagPlot("Current", ylabel='Current', yunit=pq.picoamp)
    Conductance =        TagPlot("Conductance", ylabel="Conductance")
    ConductanceDensity = TagPlot("ConductanceDensity", ylabel="ConductanceDensity", yunit=pq.milli * pq.siemens / pq.cm2 )
    StateVariable =      TagPlot("StateVariable", ylabel="StateVariable")
    StateVariableTau =   TagPlot("StateTimeConstant", yunit=pq.millisecond, ylabel="Time Constant")
    StateVariableInf =   TagPlot("StateSteadyState", ylabel="Steady State")
    Event =              TagPlot("Event", ylabel="Events")





class TagViewer(object):

    MPL_AUTO_SHOW = True

    _default_plot_specs = (
        DefaultTagPlots.Voltage,
        DefaultTagPlots.CurrentDensity,
        DefaultTagPlots.Current,
        DefaultTagPlots.Conductance,
        DefaultTagPlots.ConductanceDensity,
        DefaultTagPlots.StateVariable,
        DefaultTagPlots.StateVariableTau,
        DefaultTagPlots.StateVariableInf,
        DefaultTagPlots.Event,
       )

    _default_fig_kwargs = {'figsize': (12, 8) }

    _options_show_xlabel = ('only-once','all',  False)
    _options_show_xticklabels=('only-once','all', False)
    _options_show_xticklabels_with_units=(True,False)
    _options_show_xaxis_position = ('bottom','top')

    def __init__(
        self,
        srcs,
        plots=None,
        additional_plots=None,
        figtitle=None,
        fig_kwargs=None,
        show=True,
        linkage=None,
        timerange=None,
        mpl_tight_bounds=False,

        share_x_labels=True,

        nxticks=4, 
        show_xlabel='only-once',
        show_xticklabels='only-once',
        show_xticklabels_with_units=True,
        show_xaxis_position='bottom',
        xticks=None

        ):
        """Plot a set of traces.

        Keyword arguments:
        plots -- 
        srcs --
        plots --
        additional_plots -- 
        figtitle --
        fig_kwargs --
        show --
        linkage --
        timerange -- 
        mpl_tight_bounds --
        share_x_labels --

        nxticks=4, 
        show_xlabel -- which plots should the x-axis be displayed on.
        show_xticklabels --
        show_xticklabels_with_units -- 
        show_xaxis_position --
        xticks -- 
        """

        if fig_kwargs is None:
            fig_kwargs = self._default_fig_kwargs

        self.linkage = linkage


        if not is_iterable(srcs):
            srcs = [srcs]

        # For each type of input (in 'srcs'); this should return a list of traces:
        self.all_trace_objs = []
        self.all_event_set_objs = []
        trace_extractors = {
            SimulationResult:   lambda obj: self.all_trace_objs.extend(obj.traces),
            TraceFixedDT:       lambda obj: self.all_trace_objs.append(obj),
            TraceVariableDT:    lambda obj: self.all_trace_objs.append(obj),
            TracePiecewise:     lambda obj: self.all_trace_objs.append(obj),
            EventSet:           lambda obj: self.all_event_set_objs.append(obj)
                            }

        for obj in srcs:
            tr_extractor = trace_extractors[type(obj)]
            tr_extractor(obj)

        # Use the new PlotSpec architecture:
        # Filter out which plots are actually going to display something,
        # and filter out the rest:
        plots = plots if plots is not None else TagViewer._default_plot_specs

        if additional_plots:
            plots = tuple(list(plots) + list(additional_plots))

        self.plot_specs = [plotspec for plotspec in plots if
                            [tr for tr in self.all_trace_objs if plotspec.addtrace_predicate(tr)] or  \
                            [evset for evset in self.all_event_set_objs if plotspec.addeventset_predicate(evset)] \
                          ]


        self.fig_kwargs = fig_kwargs
        self.figtitle = figtitle
        self.mpl_tight_bounds = mpl_tight_bounds

        self.timerange = timerange
        self.share_x_labels = share_x_labels
        self.nxticks = nxticks


        # X-axis configuration:
        self.show_xlabel = show_xlabel
        self.show_xticklabels = show_xticklabels
        self.show_xticklabels_with_units = show_xticklabels_with_units
        self.show_xaxis_position = show_xaxis_position
        self.xticks=xticks
        assert self.show_xlabel in self._options_show_xlabel, 'Invalid'
        assert self.show_xticklabels in self._options_show_xticklabels
        assert self.show_xticklabels_with_units in self._options_show_xticklabels_with_units
        assert self.show_xaxis_position in self._options_show_xaxis_position 
        if is_iterable( self.xticks ) and all( [isinstance(xtick, (int, float)) for xtick in self.xticks]):
            self.xticks = [ xtick*pq.ms for xtick in self.xticks]
        assert self.xticks is None or isinstance(self.xticks, int) or ( is_iterable(self.xticks) and [ unit(xtick) for xtick in self.xticks] )


        self.fig = None
        self.subaxes = []
        self.create_figure()


        if TagViewer.MPL_AUTO_SHOW and show:
            import pylab
            pylab.show()

    def create_figure(self):
        self.fig = QuantitiesFigure(**self.fig_kwargs)

        # Add a title to the plot:
        if self.figtitle:
            self.fig.suptitle(self.figtitle)

        # Work out what traces are on what graphs:
        plotspec_to_traces = dict([(plot_spec, [tr for tr in self.all_trace_objs if plot_spec.addtrace_predicate(tr)]) for plot_spec in self.plot_specs ])
        if self.linkage:
            self.linkage.process(plotspec_to_traces)

        n_plots = len(self.plot_specs)

        for (i, plot_spec) in enumerate(self.plot_specs):

            # Create the axis:
            ax = self.fig.add_subplot(n_plots, 1, i + 1)
            ax.set_xunit(pq.millisecond)
            ax.set_xmargin(0.05)
            ax.set_ymargin(0.05)

            ax.set_xaxis_maxnlocator(self.nxticks)

            # Leave the plotting to the tag-plot object
            plot_spec.plot( ax=ax, 
                            all_traces=self.all_trace_objs, 
                            all_eventsets=self.all_event_set_objs, 
                            time_range=self.timerange, 
                            linkage=self.linkage, 
                            #plot_xaxis_details=plot_xaxis_details,

                            show_xlabel = self.show_xlabel,
                            show_xticklabels = self.show_xticklabels,
                            show_xticklabels_with_units = self.show_xticklabels_with_units,
                            show_xaxis_position = self.show_xaxis_position,
                            is_top_plot = (i==0),
                            is_bottom_plot = (i==n_plots-1),
                            xticks = self.xticks

                            )


            # Save the Axis:
            self.subaxes.append(ax)

        if self.mpl_tight_bounds:
            import pylab
            try:
                pylab.tight_layout()
            except AttributeError:
                pass  # This is version specfic
            except ValueError:
                pass # Top can't be less than bottom


