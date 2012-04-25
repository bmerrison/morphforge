#
#
#
#
#
#
#
##from StringIO import StringIO as sIO
#
#
#
#class TestMorphLocationAndDistances(unittest.TestCase):
#    def setUp(self):
#        pass
#    
#    
#    
#    def testSectionLocation(self):
#        validSimpleDict20 = {'root': { 'length':3, 'diam':4, 'region':'soma', 'id':'somaID', 'sections':[
#                                                    {'length':5, 'diam':6, 'region':'process', 'id':'processID1', 'sections':[
#                                                                   {'length':7, 'diam':8, 'region':'process', 'id':'processID1a'},
#                                                                   {'length':9, 'diam':10, 'region':'process', 'id':'processID1b'},
#                                                                                ]},
#                                                    {'length':11, 'diam':12, 'region':'process', 'id':'processID2', 'sections':[
#                                                                    {'length':13, 'diam':14, 'region':'process', 'id':'processID2a'},
#                                                                    {'length':15, 'diam':16, 'region':'process', 'id':'processID2b'},
#                                                                       ]},
#                                                                    ] } }                                        
#        
#        
#        m = MorphologyFactory.fromDictionary(validSimpleDict20, "MyCell1", {}) 
#        
#        # Check the diameters
#        self.assertAlmostEqual(SectionLength(m.getSection("somaID")), 3.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID1")), 5.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID1a")), 7.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID1b")), 9.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID2")), 11.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID2a")), 13.0, 4)
#        self.assertAlmostEqual(SectionLength(m.getSection("processID2b")), 15.0, 4)
#        
#        
#    def testSectionFarEndDistToRootCentre(self):  
#        validSimpleDict20 = {'root': { 'length':3, 'diam':4, 'region':'soma', 'id':'somaID', 'sections':[
#                                                    {'length':5, 'diam':6, 'region':'process', 'id':'processID1', 'sections':[
#                                                                   {'length':7, 'diam':8, 'region':'process', 'id':'processID1a'},
#                                                                   {'length':9, 'diam':10, 'region':'process', 'id':'processID1b'},
#                                                                                ]},
#                                                    {'length':11, 'diam':12, 'region':'process', 'id':'processID2', 'sections':[
#                                                                    {'length':13, 'diam':14, 'region':'process', 'id':'processID2a'},
#                                                                    {'length':15, 'diam':16, 'region':'process', 'id':'processID2b'},
#                                                                       ]},
#                                                                    ] } }          
#        m = MorphologyFactory.fromDictionary(validSimpleDict20, "MyCell1", {}) 
#                      
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("somaID")), 3.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID1")), 8.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID1a")), 15.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID1b")), 17.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID2")), 14.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID2a")), 27.0, 4)
#        self.assertAlmostEqual(SectionFarEndDistToRootCentre(m.getSection("processID2b")), 29.0, 4)
#        
#        
#    def testDistanceBetweenMorphLocations(self):
#        validSimpleDict20 = {'root': { 'length':3, 'diam':4, 'region':'soma', 'id':'somaID', 'sections':[
#                                                    {'length':5, 'diam':6, 'region':'process', 'id':'processID1', 'sections':[
#                                                                   {'length':7, 'diam':8, 'region':'process', 'id':'processID1a'},
#                                                                   {'length':9, 'diam':10, 'region':'process', 'id':'processID1b'},
#                                                                                ]},
#                                                    {'length':11, 'diam':12, 'region':'process', 'id':'processID2', 'sections':[
#                                                                    {'length':13, 'diam':14, 'region':'process', 'id':'processID2a'},
#                                                                    {'length':15, 'diam':16, 'region':'process', 'id':'processID2b'},
#                                                                       ]},
#                                                                    ] } }
#                  
#        m = MorphologyFactory.fromDictionary(validSimpleDict20, "MyCell1", {}) 
#        
#        ML_somaNr = MorphLocation(m.getSection("somaID"), 0.0)
#        ML_somaMid = MorphLocation(m.getSection("somaID"), 0.5)
#        ML_somaFar = MorphLocation(m.getSection("somaID"), 1.0)
#        
#        ML_p1Near = MorphLocation(m.getSection("processID1"), 0.0)
#        ML_p1Mid = MorphLocation(m.getSection("processID1"), 0.5)
#        ML_p1Far = MorphLocation(m.getSection("processID1"), 1.0)
#        
#        
#        ML_p2bNear = MorphLocation(m.getSection("processID2b"), 0.0)
#        ML_p2bNearThird = MorphLocation(m.getSection("processID2b"), 0.333333333333)
#        ML_p2bFarThird = MorphLocation(m.getSection("processID2b"), 0.666666666666)
#        ML_p2bFar = MorphLocation(m.getSection("processID2b"), 1.0)
#        
#        
#        # Distance between the same point must be zero.
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaNr, ML_somaNr), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaMid, ML_somaMid), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaFar, ML_somaFar), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Near, ML_p1Near), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Mid, ML_p1Mid), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Far, ML_p1Far), 0.0, 4)
#
#        #Distances between points on the same section:
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaNr, ML_somaMid), 1.5, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaMid, ML_somaFar), 1.5, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaNr, ML_somaFar), 3.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Near, ML_p1Mid), 2.5, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Mid, ML_p1Far), 2.5, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p1Near, ML_p1Far), 5.0, 4)
#        
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p2bNear, ML_p2bNearThird), 5.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p2bNear, ML_p2bFarThird), 10.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p2bNear, ML_p2bFar), 15.0, 4)
#        
#        
#        #Distance between end/near points on adjacent sections:
#        ML_p2Far = MorphLocation(m.getSection("processID2"), 1.0)
#        
#        print "Soma ", m.getSection("somaID").getNPA3()
#        print "SomaFar:", getMorphLocationCoords(ML_somaFar)
#        print "ML_p1Near:", getMorphLocationCoords(ML_p1Near)
#        
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaFar, ML_p1Near), 0.0, 4)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_p2Far, ML_p2bNear), 0.0, 4)
#        
#        #Distance between end points should be the lenght of the section between them:
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(ML_somaFar, ML_p2bNear), SectionLength(m.getSection("processID2")) , 4)
#        
#        
#    
#        #Check Root MorphLocation:
#        rootMorphLoc = getRootMorphLocation(m)
#        self.assertFalse(rootMorphLoc.section.isRoot())
#        self.assertTrue(rootMorphLoc.section.parent.isRoot())
#        self.assertTrue(rootMorphLoc.section == m.root.children[0])
#        self.assertTrue(rootMorphLoc.section == m.getSection("somaID"))
#        self.assertTrue(rootMorphLoc.sectionpos == 0.0)
#        self.assertAlmostEquals(DistanceBetweenMorphLocations(rootMorphLoc, ML_somaNr), 0.0, 4)
#        
#    
#    def testXYZMorphLocations(self):
#        validSimpleDict20 = {'root': { 'length':3, 'diam':4, 'region':'soma', 'id':'somaID', 'sections':[
#                                                    {'length':5, 'diam':6, 'region':'process', 'id':'processID1', 'sections':[
#                                                             {'length':7, 'diam':8, 'region':'process', 'id':'processID1a'},
#                                                             {'length':9, 'diam':10, 'region':'process', 'id':'processID1b'},
#                                                                                ]},
#                                                    {'length':11, 'diam':12, 'region':'process', 'id':'processID2', 'sections':[
#                                                             {'length':13, 'diam':14, 'region':'process', 'id':'processID2a'},
#                                                             {'length':15, 'diam':16, 'region':'process', 'id':'processID2b'},
#                                                             ]},
#                                            ] } }
#        
#        m = MorphologyFactory.fromDictionary(validSimpleDict20, "MyCell1", {})
#        rootMorphLoc = getRootMorphLocation(m)
#        ML_somaNr = MorphLocation(m.getSection("somaID"), 0.0)
#        ML_somaMid = MorphLocation(m.getSection("somaID"), 0.5)
#        ML_somaFar = MorphLocation(m.getSection("somaID"), 1.0)
#        
#        ML_p1Near = MorphLocation(m.getSection("processID1"), 0.0)
#        ML_p1Mid = MorphLocation(m.getSection("processID1"), 0.5)
#        ML_p1Far = MorphLocation(m.getSection("processID1"), 1.0)
#        
#        
#        ML_p2bNear = MorphLocation(m.getSection("processID2b"), 0.0)
#        ML_p2bNearThird = MorphLocation(m.getSection("processID2b"), 0.333333333333)
#        ML_p2bFarThird = MorphLocation(m.getSection("processID2b"), 0.666666666666)
#        ML_p2bFar = MorphLocation(m.getSection("processID2b"), 1.0)
#        
#        #TODO more tsting here:
#        if not (ML_p1Near and ML_p1Mid and ML_p1Far and ML_p2bNear and ML_p2bNearThird and ML_p2bFarThird and ML_p2bFar): print "Hello"
#        #DONE TO SUPRESS LINT
#        
#        # Check the Root Location:
#        self.assertAlmostEquals(linalg.norm(getMorphLocationCoords(rootMorphLoc) - numpy.array((0, 0, 0))), 0.0, 4)
#        self.assertAlmostEquals(linalg.norm(getMorphLocationCoords(ML_somaNr) - numpy.array((0, 0, 0))), 0.0, 4)
#        self.assertAlmostEquals(linalg.norm(getMorphLocationCoords(ML_somaMid) - numpy.array((1.5, 0, 0))), 0.0, 4)
#        self.assertAlmostEquals(linalg.norm(getMorphLocationCoords(ML_somaFar) - numpy.array((3.0, 0, 0))), 0.0, 4)
#        
#        
#    
