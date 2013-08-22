'''
Created on 22/08/2013

@author: Jesper
'''
import os
from resources import Resources

class ResourceAnalyzer(object):
    '''
    Reads resources from an Android project and generates a Resources object
    '''
    
    projectroot = None
    resourceroot = None

    dir_readers = {}
    
    debug = False
    
    def __init__(self, projectroot, debug=False):
        self.projectroot = projectroot
        if not os.path.exists( self.projectroot ):
            raise ValueError( "projectroot (%s) doesn't exist!" % ( self.projectroot ) )
        self.resourceroot = os.path.join( projectroot, 'res' )
        if not os.path.exists( self.resourceroot ) or not os.path.isdir( self.resourceroot ):
            raise ValueError( "projectroot doesn't contain a res-folder (%s)!" % ( self.resourceroot ) )
        
        self.debug = debug
        
        self._init_readers()
        
    def _init_readers(self):
        self.dir_readers['color'] = self._read_color_dir
        self.dir_readers['drawable'] = self._read_drawable_dir
        self.dir_readers['layout'] = self._read_layout_dir
        self.dir_readers['values'] = self._read_values_dir
    
    def read(self):
        self.debug_log( "Reading resources from %s" % self.projectroot )
        result = Resources()
        # Find dirs (http://stackoverflow.com/a/142535)
        for dirname in os.walk( self.resourceroot ).next()[1]:
            self._read_dir(dirname, result)
            
        return result
    
    def _read_dir(self, dirname, result):
        dirtype, qualifiers = ResourceAnalyzer.get_dir_type_and_qualifiers( dirname )
        if not self.dir_readers.has_key( dirtype ):
            return
        
        fulldir = os.path.join( self.resourceroot, dirname )
        
        reader = self.dir_readers.get( dirtype )
        reader( fulldir, qualifiers, result )
        
    def _read_color_dir(self, dirname, qualifiers, result):
        self.debug_log( "Reading colors (%s)" % ( ", ".join( qualifiers ) ) )
        self._read_resource_file_dir("colors", dirname, qualifiers, result)
        
    def _read_drawable_dir(self, dirname, qualifiers, result):
        self.debug_log( "Reading drawables (%s)" % ( ", ".join( qualifiers ) ) )
        self._read_resource_file_dir("drawables", dirname, qualifiers, result)
                
    def _read_layout_dir(self, dirname, qualifiers, result):
        self.debug_log( "Reading layouts (%s)" % ( ", ".join( qualifiers ) ) )
        self._read_resource_file_dir("layouts", dirname, qualifiers, result)
        
    def _read_values_dir(self, dirname, qualifiers, result):
        self.debug_log( "Reading values (%s)" % ( ", ".join( qualifiers ) ) )
                
    def _read_resource_file_dir(self, restype, dirname, qualifiers, result):
        for _, _, files in os.walk( dirname ):
            for filename in files:
                resname = ResourceAnalyzer.get_resource_name_from_filename( filename )
                result.add( restype, resname, qualifiers )

    def debug_log(self, msg):
        if self.debug:
            print msg

    @staticmethod
    def get_resource_name_from_filename(filename):
        return filename[:filename.index('.')]
    
    @staticmethod
    def get_dir_type_and_qualifiers(dirname):
        parts = dirname.split( "-" )
        return ( parts[0], parts[1:] )
