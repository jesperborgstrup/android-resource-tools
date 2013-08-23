'''
Created on 22/08/2013

@author: Jesper
'''
import os

from xml.dom import Node, minidom

from resources import Resources

class ResourceAnalyzer(object):
    '''
    Reads resources from an Android project and generates a Resources object
    '''
    
    projectroot = None
    manifestfile = None
    resourceroot = None

    DIR_TYPES = { 'anim': 'tween_animations', 'animator': 'property_animations',
                  'color': 'colors', 'drawable': 'drawables', 'layout': 'layouts',
                  'menu': 'menus', 'raw': 'raw', 'xml': 'xml'}
    
    ITEM_TYPES = { 'anim': 'tween_animations', 'animator': 'property_animations',
                   'attr': 'attrs', 'bool': 'booleans', 'color': 'colors',
                   'declare-styleable': 'declare_styleables', 'dimen': 'dimensions',
                   'drawable': 'drawables', 'fraction': 'fractions', 'id': 'ids',
                   'integer': 'integers', 'interpolator': 'interpolators',
                   'layout': 'layouts', 'menu': 'menus', 'mipmap': 'mipmaps',
                   'plurals': 'plurals', 'raw': 'raw', 'string': 'strings',
                   'style': 'styles', 'styleable': 'styleables', 'xml': 'xml'}
    
    debug = False
    
    def __init__(self, projectroot, debug=False):
        self.projectroot = projectroot
        if not os.path.exists( self.projectroot ):
            raise ValueError( "projectroot (%s) doesn't exist!" % ( self.projectroot ) )
        self.manifestfile = os.path.join( self.projectroot, "AndroidManifest.xml" )
        if not os.path.exists( self.manifestfile ):
            raise ValueError( "manifest (%s) doesn't exist!" % ( self.manifestfile ) )
        self.resourceroot = os.path.join( self.projectroot, 'res' )
        if not os.path.exists( self.resourceroot ):
            raise ValueError( "resourceroot (%s) doesn't exist!" % ( self.resourceroot ) )
        
        self.debug = debug
        
    def read(self):
        self.debug_log( "Reading resources from %s" % self.projectroot )
        result = Resources()
        self._read_manifestfile(result)
        # Find dirs (http://stackoverflow.com/a/142535)
        for dirname in os.walk( self.resourceroot ).next()[1]:
            self._read_dir(dirname, result)
            
        return result
    
    def _read_manifestfile(self, result):
        xml = minidom.parse( self.manifestfile )
        self._parse_manifest_element_recursive(xml.documentElement, result)
    
    def _parse_manifest_element_recursive(self, element, result):
        for attr_i in xrange( element.attributes.length ):
            attribute = element.attributes.item( attr_i )
            val = attribute.value
            if not val.startswith( '@' ) or not '/' in val or val.startswith( '@android:' ):
                continue
            
            ref_name = val[ val.index('/')+1: ].encode('ascii')
            if attribute.value.startswith( '@+' ):
                ref_type = val[ 2:val.index('/') ]
            else:
                ref_type = val[ 1:val.index('/') ]
            if not ref_type in ResourceAnalyzer.ITEM_TYPES.keys():
                print "*** Unknown element '%s' ***" % ( ref_type )
                continue
            ref_type = ResourceAnalyzer.ITEM_TYPES.get( ref_type )
                
            result.manifest_references.add( (ref_type, ref_name ) )
        for child in filter( lambda n: n.nodeType == Node.ELEMENT_NODE, element.childNodes ):
            self._parse_manifest_element_recursive(child, result)
    
    def _read_dir(self, dirname, result):
        dirtype, qualifiers = ResourceAnalyzer.get_dir_type_and_qualifiers( dirname )
        fulldir = os.path.join( self.resourceroot, dirname )
        if dirtype == 'values':
            self._read_values_dir( fulldir, qualifiers, result )
        elif ResourceAnalyzer.DIR_TYPES.has_key( dirtype ):
            restype = ResourceAnalyzer.DIR_TYPES.get( dirtype )
            self._read_resource_file_dir(restype, fulldir, qualifiers, result)
        
    def _read_resource_file_dir(self, restype, dirname, qualifiers, result):
        self.debug_log( "Readinsg %s (%s, %s)" % ( restype, ", ".join( qualifiers ), dirname ) )
        for root, _, files in os.walk( dirname ):
            for filename in files:
                print os.path.join( root, filename )
                resname = ResourceAnalyzer.get_resource_name_from_filename( filename )
                result.add( restype, resname, qualifiers )
                if filename.endswith( '.xml' ):
                    fullfilename = os.path.join( root, filename )
                    self._parse_xml_file(restype, resname, fullfilename, qualifiers, result)
#                    return
                    
    def _parse_xml_file(self, restype, resname, filename, qualifiers, result):
        xml = minidom.parse( filename )
        self.debug_log( "parsing %s, %s, %s" % ( restype, qualifiers, resname ) )
        self._parse_xml_file_element_recursive(restype, resname, xml.documentElement, qualifiers, result)
    
    def _parse_xml_file_element_recursive(self, restype, resname, element, qualifiers, result):
        for attr_i in xrange( element.attributes.length ):
            attribute = element.attributes.item( attr_i )
            val = attribute.value
            if not val.startswith( '@' ) or not '/' in val or val.startswith( '@android:' ):
                continue
            
            ref_name = val[ val.index('/')+1: ].encode('ascii')
            if attribute.value.startswith( '@+' ):
                ref_type = val[ 2:val.index('/') ]
                if not ref_type in ResourceAnalyzer.ITEM_TYPES.keys():
                    print "*** Unknown element '%s' ***" % ( ref_type )
                    continue
                ref_type = ResourceAnalyzer.ITEM_TYPES.get( ref_type )
                result.add( ref_type, ref_name, qualifiers )
            else:
                ref_type = val[ 1:val.index('/') ]
                if not ref_type in ResourceAnalyzer.ITEM_TYPES.keys():
                    print "*** Unknown element '%s' ***" % ( ref_type )
                    continue
                ref_type = ResourceAnalyzer.ITEM_TYPES.get( ref_type )
                
            result.add_reference( restype, resname, ref_type, ref_name )
        for child in filter( lambda n: n.nodeType == Node.ELEMENT_NODE, element.childNodes ):
            self._parse_xml_file_element_recursive(restype, resname, child, qualifiers, result)

    def _read_values_dir(self, dirname, qualifiers, result):
        self.debug_log( "Reading values (%s)" % ( ", ".join( qualifiers ) ) )
        for root, _, files in os.walk( dirname ):
            for filename in files:
                fullfilename = os.path.join( root, filename )
#                self.debug_log( "Parsing values file %s" % ( fullfilename ) )
                xml = minidom.parse( fullfilename )
                if xml.documentElement.tagName != 'resources':
                    continue
                self._read_resources_element( xml.documentElement, dirname, qualifiers, result )
                
    def _read_resources_element(self, element, dirname, qualifiers, result):
        for node in element.childNodes:
            if not node.nodeType is Node.ELEMENT_NODE:
                continue
            if not node.hasAttribute( 'name' ):
                continue
            if node.tagName == 'item':
                self._read_item_element(node, dirname, qualifiers, result)
                continue
            if not node.tagName in ResourceAnalyzer.ITEM_TYPES.keys():
                print "*** Unknown element '%s' ***" % ( node.tagName )
                continue
            
            name = node.getAttribute( "name" ).encode('ascii')
            result.add( ResourceAnalyzer.ITEM_TYPES.get( node.tagName ), name, qualifiers )
            
    def _read_item_element(self, element, dirname, qualifiers, result):
        if not element.hasAttribute( 'type' ):
            return
        type = element.getAttribute( 'type' )
        if not type in ResourceAnalyzer.ITEM_TYPES.keys():
            return
        
        name = element.getAttribute( "name" ).encode('ascii')
        result.add( ResourceAnalyzer.ITEM_TYPES.get( type ), name, qualifiers )
                
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
