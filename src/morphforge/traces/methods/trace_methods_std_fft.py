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
from morphforge.traces import TraceFixedDT

import numpy as np


def _fft(tr, normalise=True):
    fft_values = np.fft.fft(tr.data_pts)
    if normalise:
        fft_values /= fft_values.max()
    dt_in_s = tr.get_dt_new().rescale('s').magnitude
    ftfreq = np.fft.fftfreq(tr.data_pts.size, dt_in_s)
    return (ftfreq, fft_values)


def _psd(tr, normalise=True):
    fft_values = np.fft.fft(tr.data_pts)
    fft_values = fft_values.real() ** 2 + fft_values.imag() ** 2
    if normalise:
        fft_values /= fft_values.max()

    dt_in_s = tr.get_dt_new().rescale('s').magnitude
    ftfreq = np.fft.fftfreq(tr.data_pts.size, dt_in_s)
    return (ftfreq, fft_values)


TraceMethodCtrl.register(TraceFixedDT, 'fft', _fft, can_fallback_to_fixed_trace=True)
TraceMethodCtrl.register(TraceFixedDT, 'psd', _psd, can_fallback_to_fixed_trace=True)

