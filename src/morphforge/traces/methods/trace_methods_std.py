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

from morphforge.traces.traceobjpluginctrl import TraceMethodCtrl

import numpy as np
from morphforge.traces.tracetypes import TraceVariableDT
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes import TraceFixedDT


def _get_piecewise_linear_points(tr):
    x_unit = tr.pieces[0].get_min_time().units
    y_unit = tr.pieces[0].get_start_value().units

    x_points = []
    y_points = []

    for piece in tr.pieces:
        x_points.append(float(piece.get_min_time().rescale(x_unit).magnitude))
        x_points.append(float(piece.get_max_time().rescale(x_unit).magnitude))

        y_points.append(float(piece.get_start_value().rescale(y_unit).magnitude))
        y_points.append(float(piece.get_end_value().rescale(y_unit).magnitude))

    return (np.array(x_points) * x_unit, np.array(y_points) * y_unit)


# Plotting:
TraceMethodCtrl.register(TraceFixedDT,    'plotpoints', lambda tr: (tr.time_pts, tr.data_pts))
TraceMethodCtrl.register(TraceVariableDT, 'plotpoints', lambda tr: (tr.time_pts, tr.data_pts))
TraceMethodCtrl.register(TracePiecewise,  'plotpoints', _get_piecewise_linear_points)

