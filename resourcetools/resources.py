'''
Created on 22/08/2013

@author: Jesper
'''

class Resources(object):
    '''
    A representation of resources inside an Android project.
    
    Each resource type is a dictionary, where the resource name is the key, and the value is
    a list of qualifiers where this resource occurs
    '''
    
    tween_animations = {}
    property_animations = {}
    arrays = {}
    attrs = {}
    booleans = {}
    colors = {}
    declare_styleables = {}
    dimensions = {}
    drawables = {}
    fractions = {}
    ids = {}
    integers = {}
    interpolators = {}
    layouts = {}
    menus = {}
    mipmaps = {}
    plurals = {}
    raw = {}
    strings = {}
    styles = {}
    styleables = {}
    xml = {}
    
    _ATTRS = { 'tween_animations': 'Tween animations',
               'property_animations': 'Property animations',
               'arrays': 'Arrays',
               'attrs': 'Attributes',
               'booleans':'Booleans',
               'colors':'Colors',
               'declare_styleables':'Declare styleables',
               'dimensions':'Dimensions',
               'drawables':'Drawables',
               'fractions':'Fractions',
               'ids':'IDs',
               'integers':'Integers',
               'interpolators':'Interpolators',
               'layouts':'Layouts',
               'menus':'Menus',
               'mipmaps':'Mipmaps',
               'plurals':'Plurals',
               'raw':'Raw',
               'strings':'Strings',
               'styles':'Styles',
               'styleables':'Styleables',
               'xml':'XML',}

    def __init__(self):
        pass
    
    def dump(self):
        for attrname in sorted( Resources._ATTRS.keys() ):
            attr = getattr( self, attrname )
            if len( attr ) > 0:
                print "%s: %s" % ( Resources._ATTRS[attrname], attr )
        
    def dump_count(self):
        for attrname in sorted( Resources._ATTRS.keys() ):
            attr = getattr( self, attrname )
            if len( attr ) > 0:
                print "%s: %d" % ( Resources._ATTRS[attrname], len( attr ) )
        
    def add(self, restype, name, value):
        if not hasattr( self, restype ):
            raise ValueError( "Invalid resource type: %s" % ( restype ) )
        res = getattr(self, restype)
        if not isinstance( res, dict ):
            raise ValueError( "Invalid resource type: %s" % ( restype ) )

        if not res.has_key( name ):
            res[name] = []
            
        if value not in res[name]:
            res[name].append( value )