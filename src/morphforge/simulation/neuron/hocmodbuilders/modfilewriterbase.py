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


from Cheetah.Template import Template
from datetime import datetime






modTmplHeader = """
TITLE $title

COMMENT
Modfile Generated by morphforge:
###$__dict__
SUFFIX: $suffix
ENDCOMMENT
"""

modTmplUnits = """
UNITS {
#for ($uAbbr, $uName)  in $units.iteritems():
    ($uAbbr) = ($uName)
#end for
}
"""


modTmplInterface = """
? interface
NEURON {
    THREADSAFE
    SUFFIX $suffix
    NONSPECIFIC_CURRENT $currentname

    RANGE $rangevars

}
"""


modTmplParams = """
PARAMETER {
#for $pName,($pValue,$pUnit,$pRange) in $parameters.iteritems():
    #set $pUnitOut = "("+pUnit+")" if $pUnit else ""
    #set $pRangeOut = "<%1.1e,%1.1e>"%pRange if $pRange else ""
    $pName = $pValue $pUnitOut $pRangeOut
#end for


}
"""

modTmplState = """
STATE {
#for state in $internalstates:
    $state
#end for





#if $chlsopenequation:
    chls_open
#end if
}
"""

modTmplAssigned = """
ASSIGNED {
    v (mV)
    celsius (degC)
    $currentname (mA/cm2)

#for $rName,($rEqn,$rUnit) in $rates.iteritems():
    #set $rUnitOut = "("+rUnit+")" if $rUnit else ""
    $rName $rUnitOut
#end for

#if $conductanceequation:
    g (S/cm2)
#end if


}
"""



modTmplBreakpoints = """
? currents
BREAKPOINT {
#if $internalstates:
    SOLVE states METHOD cnexp
#end if
    $currentname = $currentequation


#if $conductanceequation:
    g = $conductanceequation
#end if
#if $chlsopenequation:
    chls_open = chlsopenequation
#end if

}
"""

modTmplInitial = """
INITIAL {
    ${updatefunctionname}(v)
#for $state, ($initialvalue, $equation) in $internalstates.iteritems():
    $state = $initialvalue
#end for

}
"""

modTmplDerivative = """
? states
DERIVATIVE states {
        ${updatefunctionname}(v)
#for $state, ($initialvalue, $equation) in $internalstates.iteritems():
    $equation
#end for
}
"""






modTmplProcedure = """

? rates
PROCEDURE ${updatefunctionname}(v(mV)) {

#set $locals = [ r[0][0] for r in $rates.values() if r[0][0] ]
#set $localString = "LOCAL " + ",".join(locals) if $locals else ""
    $localString
UNITSOFF

#for $rName in $ratecalcorder:
#set (($rEqnLocals,$rEqn),$rUnit) = $rates[$rName]
    $rEqn
#end for
}
"""


modTmplFunctions = """
$functions

UNITSON
"""



class MM_ModFileWriterBase(object):
    defaultTitle = "Untitled mod-file"
    defaultComment = "Automatically generated modfile - morphforge @ "
    default_units = { "mA":"milliamp", "mV":"millivolt", "S":"siemens", "pA":"picoamp", "um":"micrometer" }
    defaultCurrentName = "i"
    defaultupdatefunctionname = "rates"

    def __init__(self, suffix,
                 title=None,
                 internalstates=None,
                 parameters=None,
                 functions=None,
                 rates=None,
                 ratecalcorder=None,
                 currentequation=None,
                 conductanceequation=None,
                 chlsopenequation=None,
                 units=None):

        self.title = title if title else self.defaultTitle
        self.comment = self.defaultComment + datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

        self.suffix = suffix

        # {name: (initialvalue, equation) }
        self.internalstates = (internalstates if internalstates else {})

        # {name: (value, unit,range)}
        self.parameters = (parameters if parameters else {})

        # {name: ((locals, equnation),unit) }
        self.rates = (rates if rates else {})
        self.ratecalcorder = ratecalcorder if ratecalcorder else []

        #{name: code}
        self.functions = (functions if functions else "")


        self.currentname = self.defaultCurrentName
        self.units = (units if units else self.default_units)

        self.currentequation = currentequation

        self.updatefunctionname = self.defaultupdatefunctionname

        # Optional:
        self.conductanceequation = conductanceequation
        self.chlsopenequation = chlsopenequation





    def generate_modfile(self):
        assert self.currentequation

        self.rangevars = ','.join(self.parameters.keys()
                                  + self.rates.keys()
                                  + self.internalstates.keys() + ['i',
                                  'g'])


        if self.internalstates:
            blks = [
                modTmplHeader,
                modTmplUnits,
                modTmplInterface,
                modTmplParams,
                modTmplState,
                modTmplAssigned,
                modTmplBreakpoints,
                modTmplInitial,
                modTmplDerivative,
                modTmplProcedure,
                modTmplFunctions,
                ]
        elif self.conductanceequation:
            blks = [
                modTmplHeader,
                modTmplUnits,
                modTmplInterface,
                modTmplParams,
                modTmplState,
                modTmplAssigned,
                modTmplBreakpoints,
                modTmplProcedure,
                modTmplFunctions,
                ]
        else:
            blks = [
                modTmplHeader,
                modTmplUnits,
                modTmplInterface,
                modTmplParams,
                modTmplAssigned,
                modTmplBreakpoints,
                modTmplProcedure,
                modTmplFunctions,
                ]


        # Debug:
        # for blk in blks:
        #    print blk
        #    print Template(blk, [self]).respond()


        resps = [Template(blk, [self]).respond() for blk in blks ]
        return "".join(resps)

