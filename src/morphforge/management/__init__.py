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

from morphforge.simulation.neuron import NEURONEnvironment
from morphforge.simulationanalysis.summaries_new import SummariserLibrary

import inspect

try:
    import mredoc as mrd
except ImportError:
    print 'Unable to import mredoc, you will be unable to produce pdf/html summaries'


def empty_str_matrix(N, M):
    return [['' for _m in range(M)] for _n in range(N)]


def to_symbol(chl, env):
    return ('X' if chl in env else '-')


class PluginMgr(object):

    _environments = [NEURONEnvironment]

    @classmethod
    def _get_all_from_envs(cls, extract_functor):
        objs = []
        for env in cls._environments:
            objs.extend(extract_functor(env))
        return sorted(objs, key=lambda m: m.__name__)

    @classmethod
    def get_all_chls(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.channels.keys() )

    @classmethod
    def get_all_iclamps(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.currentclamps.keys() )

    @classmethod
    def get_all_vclamps(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.voltageclamps.keys() )
    @classmethod
    def get_all_presynmechs(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.presynapticmechanisms.keys() )

    @classmethod
    def get_all_postsynmechs(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.postsynapticmechanisms.keys() )





    @classmethod
    def summarise_all(cls):
        return mrd.SectionNewPage('Morphforge Configuration',
                cls.summarise_channels(),
                cls.summarise_currentclamps(),
                cls.summarise_voltageclamps(),
                cls.summarise_presynapticmechs(),
                cls.summarise_postsynapticmechs(),
                cls.summarise_tracemethods(),
                )


    @classmethod
    def summarise_channels(cls):
        mech_types = cls.get_all_chls()
        col1 = ['Channel Name'] + [mech.__name__ for mech in mech_types]
        cols = [[env._env_name] + [to_symbol(mech, env.channels) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] + [to_symbol(mech, SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Channels', mrd.VerticalColTable(rows[0], rows[1:]))

    @classmethod
    def summarise_currentclamps(cls):
        mech_types = cls.get_all_iclamps()
        col1 = ['Clamp Name'] + [mech.__name__ for mech in mech_types]
        cols = [[env._env_name] + [to_symbol(mech, env.currentclamps) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] + [to_symbol(mech, SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Current Clamps', mrd.VerticalColTable(rows[0], rows[1:]))

    @classmethod
    def summarise_voltageclamps(cls):
        mech_types = cls.get_all_vclamps()
        col1 = ['Clamp Name'] + [mech.__name__ for mech in mech_types]
        cols = [[env._env_name] + [to_symbol(mech, env.voltageclamps) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] + [to_symbol(mech, SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Voltage Clamps', mrd.VerticalColTable(rows[0], rows[1:]))

    @classmethod
    def summarise_presynapticmechs(cls):
        mech_types = cls.get_all_presynmechs()
        col1 = ['PreSynMech'] + [mech.__name__ for mech in mech_types]
        cols = [[env._env_name] + [to_symbol(mech, env.presynapticmechanisms) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] + [to_symbol(mech, SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Presynaptic Mechanisms', mrd.VerticalColTable(rows[0], rows[1:]))

    @classmethod
    def summarise_postsynapticmechs(cls):
        mech_types = cls.get_all_postsynmechs()
        col1 = ['PostSynMech'] + [mech.__name__ for mech in mech_types]
        cols = [[env._env_name] + [to_symbol(mech, env.postsynapticmechanisms) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] + [to_symbol(mech, SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Postsynaptic Mechanisms', mrd.VerticalColTable(rows[0], rows[1:]))

    @classmethod
    def summarise_tracemethods(cls):
        return TraceLibSummariser.summarise_all()



from morphforge.traces import TraceFixedDT, TraceVariableDT, TracePiecewise
from morphforge.traces import TraceOperatorCtrl, TraceMethodCtrl
import operator

operators = ((operator.__add__, '+'), (operator.__sub__, '-'),
             (operator.__mul__, '*'), (operator.__div__, '/'),
             (operator.__pow__, r'$\textrm{exp}$') )



class TraceLibSummariser(object):

    _trace_types = [TraceFixedDT, TraceVariableDT, TracePiecewise]

    @classmethod
    def summarise_all(cls):
        return mrd.Section('Traces',
                cls.summarise_methods(),
                cls.summarise_operators(),
                mrd.Paragraph('asda'))



    @classmethod
    def _get_all_operator_types(cls):
        types = set()
        for (_operator_type, lhs_type, rhs_type) in TraceOperatorCtrl.trace_operators_all:
            types.add(lhs_type)
            types.add(rhs_type)
        return sorted(list(types), key=lambda obj:(obj not in cls._trace_types, obj.__name__))

    @classmethod
    def _get_all_trace_method_names(cls):
        methods = set()
        for (_trace_type, method_name) in TraceMethodCtrl.registered_methods:
            methods.add(method_name)
        return sorted(list(methods))
    @classmethod
    def summarise_operators(cls):

        all_types = cls._get_all_operator_types()
        trace_types = cls._trace_types
        summary_matrix = empty_str_matrix(N=len(all_types) + 1, M=len(all_types) + 1)


        for (i, tp1) in enumerate(all_types):
            summary_matrix[0][i + 1] = tp1.__name__
            summary_matrix[i + 1][0] = tp1.__name__
            for (j, tp2) in enumerate(all_types):

                # Neither of the operand is a trace_type:
                if tp1 not in trace_types and tp2 not in trace_types:
                    summary_matrix[i + 1][j + 1] = '==='
                    continue

                for (op, sym) in operators:
                    if (op, tp1, tp2) in TraceOperatorCtrl.trace_operators_all:
                        summary_matrix[i + 1][j + 1] += sym

        return mrd.Section('TraceOperators',
                           mrd.VerticalColTable(summary_matrix[0], summary_matrix[1:], caption='Operators')
                           )



    @classmethod
    def summarise_methods(cls):
        trace_types = cls._trace_types
        method_names = cls._get_all_trace_method_names()

        def get_argments(method, trace_type):
            if not TraceMethodCtrl.has_method(trace_type, method):
                return None
            functor = TraceMethodCtrl.get_method(trace_type, method)
            (args, varargs, varkw, defaults) = inspect.getargspec(functor)
            return inspect.formatargspec(args=args[1:], varargs=varargs, varkw=varkw, defaults=defaults)

        def get_argments_TraceFixedDT(method):
            return str(get_argments(method, TraceFixedDT))

        def get_docstring(method):
            trace_type = TraceFixedDT
            if not TraceMethodCtrl.has_method(trace_type, method):
                return '<None>'
            func = TraceMethodCtrl.get_method(trace_type, method)
            return inspect.getdoc(func)

        def _support_for_method(trace_type, method_name):
            if (trace_type, method_name) in TraceMethodCtrl.registered_methods:
                return 'X'
            if method_name in TraceMethodCtrl.fallback_to_fixedtrace_methods:
                return '<via fixed>'

        arguments = [get_argments_TraceFixedDT(method_name) for method_name in method_names]
        docstrings = [get_docstring(method_name) for method_name in method_names]

        col1 = [''] + method_names
        col2 = [[trace_type.__name__] + [_support_for_method(trace_type, method_name) for method_name in method_names] for trace_type in trace_types]
        col_args = ['args'] + arguments
        col_docstrings = ['docstring'] + docstrings
        cols = [col1] + col2 + [col_args] + [col_docstrings]
        rows = zip(*cols)
        tbl = mrd.VerticalColTable(rows[0], rows[1:], caption='Operators')
        return mrd.Section('TraceMethods', tbl)
