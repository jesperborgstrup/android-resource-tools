'''
Created on 22/08/2013

@author: Jesper
'''
import os

from resources import Resources
from fnmatch import fnmatch
import codecs
import re

class JavaAnalyzer(object):
    '''
    Reads Java source files from an Android project and generates a list of
    resources used in the source code
    '''
    
    srcroot = None
    
    debug = False
    r_pattern = None
    
    R_SUBCLASSES = { 'anim': 'tween_animations', 'animator': 'property_animations',
                     'attr': 'attrs', 'bool': 'booleans', 'color': 'colors',
                     'declare_styleable': 'declare_styleables', 'dimen': 'dimensions',
                     'drawable': 'drawables', 'fraction': 'fractions', 'id': 'ids',
                     'integer': 'integers', 'interpolator': 'interpolators',
                     'layout': 'layouts', 'menu': 'menus', 'mipmap': 'mipmaps',
                     'plurals': 'plurals', 'raw': 'raw', 'string': 'strings',
                     'style': 'styles', 'styleable': 'styleables', 'xml': 'xml'}
    
    def __init__(self, srcroot, debug=False):
        self.srcroot = srcroot
        if not os.path.exists( self.srcroot ):
            raise ValueError( "srcroot (%s) doesn't exist!" % ( self.srcroot ) )
        
        self.r_pattern = re.compile( r"R\.(%s).(\w+)" % ( "|".join( JavaAnalyzer.R_SUBCLASSES.keys() ) ) )
        self.debug = debug
        
    def read(self):
        self.debug_log( "Reading Java resource references from %s" % self.srcroot )
        print self.r_pattern.pattern
        print dir( self.r_pattern )
        reachable_resources = {}
        # Find dirs (http://stackoverflow.com/a/142535)
        for root, _, filenames in os.walk( self.srcroot ):
            for filename in filenames:
                if not fnmatch( filename, '*.java' ):
                    continue
                
                fullfilename = os.path.join( root, filename )
                filecontent = ""
                with codecs.open( fullfilename, 'r', 'utf8' ) as f:
                    filecontent = f.read()

                matches = self.r_pattern.findall( filecontent )
                if len( matches ) > 0:
                    for match in matches:
                        restype = match[0].encode('ascii')
                        resname = match[1]
                        if not reachable_resources.has_key( restype ):
                            reachable_resources[restype] = set()
                        reachable_resources[restype].add( resname )
                        
        return reachable_resources
    
    def debug_log(self, msg):
        if self.debug:
            print msg

