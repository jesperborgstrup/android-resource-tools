'''
Created on 22/08/2013

@author: Jesper
'''
import copy
import os

from javaanalyzer import JavaAnalyzer
from resourceanalyzer import ResourceAnalyzer

class AndroidAnalyzer(object):
    '''
    DOCSTRING!!!
    '''
    
    projectroot = None
    srcroot = None
    
    javaanalyzer = None
    resanalyzer = None
    
    debug = False
    
    def __init__(self, projectroot, debug=False):
        self.projectroot = projectroot
        if not os.path.exists( self.projectroot ):
            raise ValueError( "projectroot (%s) doesn't exist!" % ( self.projectroot ) )
        
        self.srcroot = os.path.join( self.projectroot, "src" )
        
        self.debug = debug
        
        self.javaanalyzer = JavaAnalyzer(self.srcroot, self.debug)
        self.resanalyzer = ResourceAnalyzer(self.projectroot, self.debug)

    def count_resources(self):
        resources = self.resanalyzer.read()
        print resources.dump_count()

    def find_unused_resources(self):        
        resources = self.resanalyzer.read()
        java_refs = self.javaanalyzer.read_resource_references()
        
        unused_resources = copy.deepcopy( resources.resources )
        for reftype, refname in resources.manifest_references:
            self._mark_as_used_resource(reftype, refname, resources.references, unused_resources)
        for reftype in java_refs.keys():
            for refname in java_refs[ reftype ]:
                self._mark_as_used_resource( reftype, refname, resources.references, unused_resources)

#        print unused_resources.keys()            
        for reftype in unused_resources.keys():
            if len( unused_resources[ reftype ] ) == 0:
                unused_resources.pop( reftype )
        return unused_resources
                    
    def _mark_as_used_resource(self, restype, resname, resource_refs, unused_resources):
        if resource_refs.has_key( restype ) and resource_refs[ restype ].has_key( resname ):
            refs = resource_refs[ restype ][ resname ]
            for reftype, refname in refs:
                self._mark_as_used_resource(reftype, refname, resource_refs, unused_resources)
            
        if unused_resources.has_key( restype ):
            if unused_resources[ restype ].has_key( resname ):
                unused_resources[ restype ].pop( resname )
                    
    def dump_unused_resources(self):
        unused_resources = self.find_unused_resources()
        for reftype in unused_resources.keys():
            print "=== %s ===" % reftype
            for refname in unused_resources[ reftype ].keys():
                print "- %s" % ( refname )
                    
    
    def debug_log(self, msg):
        if self.debug:
            print msg

