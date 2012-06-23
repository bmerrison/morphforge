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
import numpy as np

import os


from morphforge.core.quantities import unit
from morphforge.stdimports import LocMgr

from mhlibs.quantities_plot import QuantitiesFigure

from morphforge.morphology.visitor import SectionIndexerDF
from morphforge.simulationanalysis.summaries.reportlabconfig import ReportLabConfig
from morphforge.simulationanalysis.summaries.mmsummariser import MembraneMechanismSummariser
from morphforge.core.objectnumberer import ObjectLabeller

from collections import defaultdict





class SS_Sections(object):
    Overview = "Overview"
    KeyTraces = "KeyTraces"
    Cells = "Cells"
    GapJunctions = "Gap Junctions"
    Synapses = "Synapses"


    AppendixMembranes = "AppendixMembranes"

    ordered = [Overview, Cells, GapJunctions, Synapses,  KeyTraces, AppendixMembranes]







class SimulationSummariser(object):



    def __init__(self, simulationresult, filename=None, key_tracesets = [], make_graphs=True ):

        if not filename:
            filename = ObjectLabeller.get_next_unamed_object_name(SimulationSummariser, prefix='SimulationSummary') + '.pdf'


        self.simulationresult = simulationresult
        self.simulation = simulationresult.simulation


        self.make_graphs= make_graphs

        self.elements = defaultdict(list)

        self.key_tracesets = key_tracesets

        self.reportlabconfig = ReportLabConfig()


        # Do the Summarising:
        self.summarise(filename)



    def summarise(self, filename):
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate

        # Generate the content for each section:
        self.elements[SS_Sections.Overview].extend( self.summarise_overview() )
        self.elements[SS_Sections.KeyTraces].extend( self.summarise_key_traces() )
        self.elements[SS_Sections.Cells].extend( self.summarise_cells() )
        self.elements[SS_Sections.GapJunctions].extend( self.summarise_gapjunctions() )
        self.elements[SS_Sections.Synapses].extend( self.summarise_synapses() )

        self.elements[SS_Sections.AppendixMembranes].extend( self.summarise_appendix_membranes() )



        # Reconstruct a list all the elements from all sections:
        elements = []
        for sect in SS_Sections.ordered:
            elements.extend(self.elements[sect] )

        # Build PDF:
        dname, fname = os.path.split(filename)
        LocMgr.ensure_dir_exists(dname)
        doc = SimpleDocTemplate(filename,
                                pagesize=A4,
                                leftMargin=25,
                                rightMargin=25,
                                topMargin=25,
                                bottomMargin=25
                                )
        doc.build(elements)




    def summarise_overview(self):
        from reportlab.platypus import Paragraph, Table, PageBreak
        local_elements = []

        local_elements.append( Paragraph("Overview", self.reportlabconfig.styles['Heading1'] ) )


        # Cells:
        ########
        local_elements.append( Paragraph("Cells", self.reportlabconfig.styles['Heading2'] ) )
        table_header = ['Cell',  'Total Surface Area', 'Sections', 'Segments','Active Channels (id,[Name])']
        data = [table_header, ]

        for cell in self.simulation.get_cells():
            a = sum([ s.get_area() for s in cell.morphology]) * unit("1:um2")
            n_sections = len( cell.morphology )
            n_segments = sum( [cell.get_segmenter().get_num_segments(section) for section in cell.morphology] )
            active_mechs = cell.get_biophysics().get_all_mechanisms_applied_to_cell()
            active_chl_list = "\n".join( ["%s [%s]"%(am.get_mechanism_id(), am.name) for am in active_mechs] )
            data.append( [ cell.name, a, n_sections, n_segments, active_chl_list ] )

        local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )


        # Stimulae: CC
        ###############
        if self.simulation.get_currentclamps():
            local_elements.append( Paragraph("Current Clamps", self.reportlabconfig.styles['Heading2'] ) )
            table_header = ['Name', 'Location', 'Delay', 'Amplitude', 'Duration']
            data = [table_header, ]
            for cc in self.simulation.get_currentclamps():
                cellname = cc.celllocation.cell.name
                data.append( [ cc.name, cellname, cc.delay, cc.amp, cc.dur ] )

            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )


        # Stimulae: VC
        ###############
        if self.simulation.get_voltageclamps():
            local_elements.append( Paragraph("Voltage Clamps", self.reportlabconfig.styles['Heading2'] ) )
            table_header = ['Name', 'Location', 'Dur1', 'Dur2', 'Dur3', 'Amp1','Amp2','Amp3']
            data = [table_header, ]
            for vc in self.simulation.get_voltageclamps():
                cellname = vc.celllocation.cell.name
                data.append( [ vc.name, cellname, vc.dur1, vc.dur2, vc.dur3, vc.amp1, vc.amp2, vc.amp3 ] )

            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )


        # Finish Up:
        local_elements.append( PageBreak() )
        return local_elements



    def summarise_cells(self):
        from reportlab.platypus import  Paragraph, Table, PageBreak,Spacer
        from reportlab.lib.units import mm

        local_elements = []
        local_elements.append( Paragraph("Cells Details", self.reportlabconfig.styles['Heading1'] ) )

        for cell in self.simulation.get_cells():
            local_elements.append( Paragraph(cell.name, self.reportlabconfig.styles['Heading2'] ) )

            ##Summary:
            local_elements.append( Paragraph("Overview", self.reportlabconfig.styles['Heading3'] ) )
            data = [
                    ["Name", "value" ],
                    ["Total Area", sum([s.get_area() for s in cell.morphology]) * unit("1:um2") ],
                    ["Regions", ", ".join([ rgn.name for rgn in cell.get_regions() ]) ],
                    ["idTags", ",".join( cell.morphology.get_idtags() )],
                    ]
            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )


            local_elements.append( Spacer(1,5*mm) )


            # Data about the size of each region - makes it easy to check the soma size:
            local_elements.append( Paragraph("MorphologyTree", self.reportlabconfig.styles['Heading3'] ) )
            data = [ ["Region", "n_segments", "Area" ],     ]
            for region in cell.get_regions():
                data.append( [region.name, "%d"%len(region.sections), sum([s.get_area() for s in region.sections] ) ] )
            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )



            local_elements.append( Spacer(1,5*mm) )


            # Membrane Mechanisms:
            data = [ ["Mechanism", "Targettor", "Applicator" ],     ]
            for mta in cell.get_biophysics().get_applied_mtas():
                m = mta.mechanism.name
                t = mta.targetter.get_description()
                a = mta.applicator.get_description()
                data.append( [m,t,a] )
            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )



            ## Section Overview:
            local_elements.append( Paragraph("Sections", self.reportlabconfig.styles['Heading3'] ) )
            data = [ ["Section","Parent", "Region", "ID", "Radius (Proximal)", "Radius (Distal)", "Length", "Area", "n_segments" ], ]

            si = SectionIndexerDF(cell.morphology)()
            for section in cell.morphology:

                section_id = si[section]
                parent_id = si[section.parent] if not section.is_a_root_section() else "[NA]"
                rgn = section.region.name if section.region else "-"
                idtag = section.idtag if section.idtag else "-"
                n_segments = cell.get_segmenter().get_num_segments(section)
                data.append( [ section_id, parent_id, rgn, idtag, "%2.2f"%section.p_r, "%2.2f"%section.d_r, "%2.2f"%section.get_length(), section.get_area(), n_segments ] )

            local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )



        local_elements.append( PageBreak() )
        return local_elements


    def summarise_gapjunctions(self):
        from reportlab.platypus import Paragraph, Table, PageBreak
        from morphforgecontrib.morphology.util.util import cell_location_distance_from_soma

        local_elements = []
        local_elements.append( Paragraph("Gap Junctions", self.reportlabconfig.styles['Heading1'] ) )
        gap_junctions = self.simulation.get_gapjunctions()



        data = [ ["Cell1", "Cell2", "Resistance","Distance Soma1","Distance Soma2","PrePostDist" ]]
        for gj in gap_junctions:
            cell1_name = gj.celllocation1.cell.name
            cell2_name = gj.celllocation2.cell.name
            resistance = gj.resistance.rescale("MOhm")
            cell1_distance = cell_location_distance_from_soma( gj.celllocation1 )
            cell2_distance = cell_location_distance_from_soma( gj.celllocation2 )

            print "GJ1:", gj.celllocation1.morphlocation.get_3d_position()
            print "GJ2:", gj.celllocation2.morphlocation.get_3d_position()

            pre_post_dist = np.linalg.norm( (gj.celllocation1.morphlocation.get_3d_position() - gj.celllocation2.morphlocation.get_3d_position() ) )
            print "[Pre-Post Dist [If geometry is correct, should be 0.0]", pre_post_dist

            r = "[%s %s]"%( str(gj.celllocation1.morphlocation.get_3d_position()), str(gj.celllocation2.morphlocation.get_3d_position()) )
            print r
            print  "Cell1Section:", gj.celllocation1.morphlocation.section
            print  "Cell2Section:", gj.celllocation2.morphlocation.section
            print  "SectionPos1:", gj.celllocation1.morphlocation.sectionpos
            print  "SectionPos2:", gj.celllocation2.morphlocation.sectionpos
            print

            data.append( [cell1_name,cell2_name, str(resistance), cell1_distance, cell2_distance, pre_post_dist,r  ] )

        local_elements.append( Table(data, style=self.reportlabconfig.defaultTableStyle) )

        local_elements.append( PageBreak() )
        return local_elements

    def summarise_synapses(self):
        from reportlab.platypus import Paragraph, PageBreak
        local_elements = []
        local_elements.append( Paragraph("Synapses", self.reportlabconfig.styles['Heading1'] ) )

        local_elements.append( PageBreak() )
        return local_elements


    def summarise_key_traces(self):
        from reportlab.platypus import Paragraph, PageBreak
        if not self.make_graphs:
            return []

        local_elements = []
        local_elements.append( Paragraph("Key-Traces", self.reportlabconfig.styles['Heading1'] ) )

        for traceSetName, keyTraces in self.key_tracesets:
            local_elements.append( Paragraph("TraceSet: %s"%traceSetName, self.reportlabconfig.styles['Heading2'] ) )



            f = QuantitiesFigure(figsize=self.reportlabconfig.imagesize)
            width,height =self.reportlabconfig.imagesize
            ax = f.add_subplot(111,  ylabel="?", xlabel="time")
            for trName in keyTraces:
                tr = self.simulation.result.get_trace(trName)
                ax.plotTrace( tr )
            ax.legend()
            #localElements.append( self.reportlabconfig.save_mpl_to_rl_image( f, "KeyTrace") )


        local_elements.append( PageBreak() )
        return local_elements




    def summarise_appendix_membranes(self):
        from reportlab.platypus import Paragraph, PageBreak
        local_elements = []
        local_elements.append( Paragraph("Membrane Definitions", self.reportlabconfig.styles['Heading1'] ) )


        mechanisms = []
        for cell in self.simulation.get_cells():
            for mta in cell.get_biophysics().get_applied_mtas():
                mechanisms.append(mta.mechanism)

                #Do we already ahve the machanism, possibly with different targetters and selectors:
                #if not [ True for m in mechanisms if m ]

        # Summarise Each Membrane
        for mechanism in mechanisms:
            local_elements.append( Paragraph(mechanism.name, self.reportlabconfig.styles['Heading2'] ) )
            local_elements.extend( MembraneMechanismSummariser.summarise_membranemechanism( mechanism, self.reportlabconfig, make_graphs=self.make_graphs )  )
            local_elements.append( PageBreak() )

        return local_elements


