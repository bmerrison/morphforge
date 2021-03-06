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

from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections


class HocModUtils(object):

    initial_buffer_size = 50000

    _tmpl_str_record_modvariable = """
    objref $recVecName
    $recVecName = new Vector()
    ${recVecName}.buffer_size(%d)
    ${recVecName}.record(& ${cellname}.internalsections[${sectionindex}].${modvariable}_${neuron_suffix} ($sectionpos))
    """ % initial_buffer_size

    @classmethod
    def create_record_from_modfile(cls, hocfile_obj, vecname, cell_location, modvariable, mod_neuronsuffix, recordobj  ):

        cell = cell_location.cell
        section = cell_location.morphlocation.section
        sectionpos = cell_location.morphlocation.sectionpos
        cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
        section_index = cell_hoc['section_indexer'][section]

        data = {
            'cellname': cell_hoc['cell_name'],
            'sectionindex': section_index,
            'sectionpos': sectionpos,
            'neuron_suffix': mod_neuronsuffix,
            'recVecName': vecname,
            'modvariable': modvariable,
            }

        # Create the Cell Topology Template:
        hocfile_obj.add_to_section(MHOCSections.InitRecords,   Template(HocModUtils._tmpl_str_record_modvariable, data).respond())

        # Save the data about this cell:
        hocfile_obj[MHocFileData.Recordables][recordobj] = data




    _tmpl_str_record_hoc = """
        objref $recVecName
        $recVecName = new Vector()
        ${recVecName}.buffer_size(%d)
        ${recVecName}.record(& ${objname}.${objvar})
        """ % initial_buffer_size
    @classmethod
    def create_record_from_object(cls, hocfile_obj, vecname, objname, objvar, recordobj):

        data = {'recVecName': vecname,
                'objname': objname,
                'objvar': objvar}

        # Create the Cell Topology Template:
        sect_text = Template(HocModUtils._tmpl_str_record_hoc, data).respond()
        hocfile_obj.add_to_section(MHOCSections.InitRecords,
                                   sect_text)

        # Save the data about this cell:
        hocfile_obj[MHocFileData.Recordables][recordobj] = data


