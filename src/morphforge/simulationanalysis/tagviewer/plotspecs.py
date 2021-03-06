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

import numpy as np
from morphforge.core import unit, is_iterable
import quantities as pq

from morphforge.traces import TagSelector


def is_number_roundable_to(num, n):
    return abs(num - round(num, n)) < 0.000000001


def get_max_rounding(num):
    for i in range(0, 10):
        if is_number_roundable_to(num, i):
            return i
    assert False


def float_list_to_string(seq):
    for obj in seq:
        assert isinstance(obj, (int, float))
    roundings = [get_max_rounding(obj) for obj in seq]
    max_round = max(roundings)
    return ['%.*f' % (max_round, obj) for obj in seq]


def default_legend_labeller(tr):
    if tr.comment:
        return tr.comment
    elif tr.name:
        return tr.name
    else:
        return None


class YAxisConfig(object):


    # NOTE: ynticks is deprecated! It shoudl be moved into yticks.

    def __init__(
        self,
        yunit=None,
        yrange=None,
        ylabel=None,
        yticks=None,
        yticklabels=None,
        ymargin=None,

        show_yticklabels=True,
        show_yticklabels_with_units=False,
        ):
        self.yrange = yrange
        self.yunit = yunit
        self.ylabel = ylabel
        self.show_yticklabels=show_yticklabels
        self.show_yticklabels_with_units=show_yticklabels_with_units


        # NOTE: ynticks is deprecated! It shoudl be moved into yticks.
        self.yticks = (yticks if yticks is not None else 5)

        self.yticklabels = yticklabels
        self.ymargin = ymargin


    def format_axes(self, ax):


        ax.set_ylabel(self.ylabel)
        if self.yrange is not None:
            ax.set_ylim(self.yrange)
        if self.yunit is not None:
            #print 'Setting yunit', self.yunit
            ax.set_display_unit(y=self.yunit)


        if self.yticks is not None:
            if isinstance( self.yticks, int):
                ax.set_yaxis_maxnlocator(self.yticks)
            elif is_iterable(self.yticks):

                #print 'yticks', self.yticks
                ax.set_yticks(self.yticks)
            else:
                assert False


        if self.show_yticklabels:
            #print 'yticks', ax.get_yticks()
            ylocs = [float(ytick.rescale(ax.xyUnitDisplay[1])) for ytick in ax.get_yticks()]
            # This call makes sure that we only display as many deciaml places as is sensible.
            yticklabels = float_list_to_string(ylocs)
            ax.set_yticklabels(yticklabels, include_unit=self.show_yticklabels_with_units)
        else:
            ax.set_yticklabels('')

            
        #TODO: Something funky is going on and this is not making a difference
        if self.ymargin is not None:
            ax.set_ymargin(self.ymargin)


class TagPlot(object):

    def __init__(
        self,
        s,
        title=None,
        legend_labeller=default_legend_labeller,
        colors=None,
        event_marker_size=None,
        time_range=None,
        ylabel=None,
        yrange=None,
        yunit=None,
        yaxisconfig=None,
        yticks=None,
        ymargin=None,

        show_yticklabels=True,
        show_yticklabels_with_units=False,
        ):

        if yaxisconfig is None:
            self.yaxisconfig = YAxisConfig(ylabel=ylabel if ylabel is not None else s,
                                         yunit=yunit,
                                         yrange=yrange,
                                         yticks=yticks,
                                         ymargin=ymargin,
                                         show_yticklabels=show_yticklabels,
                                         show_yticklabels_with_units=show_yticklabels_with_units,
                                         )
        else:
            self.yaxisconfig = yaxisconfig

        self.title = title
        self.legend_labeller = legend_labeller
        self.colors = colors

        self.event_marker_size = event_marker_size
        self.time_range = time_range

        if isinstance(s, TagSelector):
            self.selector = s
        elif isinstance(s, basestring):
            self.selector = TagSelector.from_string(s)
        else:
            assert False

    # Used by TagViewer
    def addtrace_predicate(self, trace):
        return self.selector(trace)

    def addeventset_predicate(self, trace):
        return self.selector(trace)

    # Plot in order by name; this is normally fine, since annonymous objects
    # will be plotted in the order they were created.
    @classmethod
    def _sort_traces(cls, traces):
        return sorted(traces, key=lambda trace: trace.name)

    @classmethod
    def _sort_eventsets(cls, event_sets):
        return sorted(event_sets, key=lambda trace: trace.name)

    def _plot_trace(self, trace,  ax, index, color=None):
        plot_kwargs = {}

        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(trace)

        if color is not None:
            plot_kwargs['color'] = color
        else:
            if self.colors:
                plot_kwargs['color'] = self.colors[index % len(self.colors)]

        plt_tr = ax.plotTrace(trace, **plot_kwargs)
        return plt_tr

    def _plot_eventset(self, eventset, ax, index):
        if len(eventset) == 0:
            return []

        plot_kwargs = {}
        if self.event_marker_size:
            plot_kwargs['markersize'] = self.event_marker_size

        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(eventset)

        if 'label' in plot_kwargs:
            assert isinstance(plot_kwargs['label'], basestring)

        i_range = 0.2
        i_scale = i_range / len(list(eventset.times))

        data = np.array([(time.rescale("ms").magnitude, index + i * i_scale) for (i, time) in enumerate(eventset.times)])



        plot_points = ax.plot(data[:, 0] * pq.ms, data[:, 1] * pq.dimensionless, 'o', ms=2, **plot_kwargs)
        return plot_points




    def plot(self, ax, all_traces,  all_eventsets,  show_xlabel, show_xticklabels, show_xticklabels_with_units, show_xaxis_position, is_top_plot, is_bottom_plot, xticks, time_range=None, linkage=None) :

        if self.time_range is not None:
            time_range = self.time_range

        # Which traces are we plotting (rely on a mixon class):
        trcs = [trace for trace in all_traces if self.addtrace_predicate(trace)]
        eventsets = [trace for trace in all_eventsets
                     if self.addeventset_predicate(trace)]

        # Sort and plot:
        for index, trace in enumerate(self._sort_traces(trcs)):
            #color = linkage.color_allocations.get(trace, None) if linkage else None
            color = linkage.get_trace_color(trace) if linkage else None
            self._plot_trace(trace, ax=ax, index=index, color=color)


        for index, event_set in enumerate(self._sort_eventsets(eventsets)):
            self._plot_eventset(event_set,  ax=ax, index=index+len(trcs))

            # ax.set_ylim(((-0.5) * pq.dimensionless, (len(eventsets)+0.5) * pq.dimensionless))

        if len(trcs) == 0:
            padding = 0.5
            ax.set_yunit(1 * pq.dimensionless)
            ax.set_ylim(((-padding) * pq.dimensionless, (len(eventsets) - 1 + padding) * pq.dimensionless))

        # Legend:
        if self.legend_labeller is not None:
            import math
            import __builtin__ as BI
            ncols = BI.max(int(math.floor(len(trcs) / 5.0)), 1)
            ax.legend(ncol=ncols)

        if self.title is not None:
            ax.set_title(self.title)

        # Setup the x-axis:
        if time_range is not None:
            ax.set_xlim(time_range)

        # Setup the x-ticks
        if xticks is not None:
            if isinstance(xticks, int):
                ax.set_xaxis_maxnlocator(xticks)
            else:
                ax.set_xticks(xticks)

        # Should we plot xaxis-info at all?:
        if is_top_plot and show_xaxis_position == 'top':
            xaxis_position = 'top'
        elif is_bottom_plot and show_xaxis_position == 'bottom':
            xaxis_position = 'bottom'
        else:
            xaxis_position = None

        # Set the ticks & labels to be bottom or top
        if xaxis_position is not None:
            ax.set_xaxis_ticks_position(xaxis_position)
            ax.set_xaxis_label_position(xaxis_position)

        # Plot the axis-label, if
        # show_ticklabels=='all' OR show_ticklabels=='only-once' AND xaxis_position is not None:
        if show_xlabel == 'all' or show_xlabel == 'only-once' \
            and xaxis_position is not None:
            ax.set_xlabel('Time')
        else:
            ax.set_xlabel('')
            #assert False

        # Similarly, plot the axis-ticklabel, if
        if show_xticklabels == 'all' or \
			show_xticklabels == 'only-once' and xaxis_position is not None:
            ms_times = [float(x.rescale('ms')) for x in ax.get_xticks()]
            # This call makes sure that we only display as many deciaml places as is sensible.
            ts = float_list_to_string(ms_times)
            ax.set_xticklabels(ts, include_unit=show_xticklabels_with_units)

        else:
            
            ax.set_xticklabels('')

        # Setup the y-axis:
        self.yaxisconfig.format_axes(ax)

        # Turn the grid on:
        ax.grid('on')


