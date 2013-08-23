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
    
    resources = {}
    references = {}
    manifest_references = set()
    
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
        for restype in Resources._ATTRS.keys():
            self.resources[restype] = {}
    
    def dump(self):
        for attrname in sorted( self.resources.keys() ):
            attr = self.resources[ attrname ]
            if len( attr ) > 0:
                print "%s: %s" % ( Resources._ATTRS[attrname], attr )
        
    def dump_count(self):
        for attrname in sorted( self.resources.keys() ):
            attr = self.resources[ attrname ]
            if len( attr ) > 0:
                print "%s: %d" % ( Resources._ATTRS[attrname], len( attr ) )
        
    def add(self, restype, name, value):
        if not Resources._ATTRS.has_key( restype ):
            raise ValueError( "Invalid resource type: %s" % ( restype ) )
        res = self.resources[ restype ]

        if not res.has_key( name ):
            res[name] = []
            
        if value not in res[name]:
            res[name].append( value )
            
    def add_reference(self, from_restype, from_resname, to_restype, to_resname):
        if not self.resources.has_key( from_restype ):
            raise ValueError( "Invalid resource type: %s" % ( from_restype ) )
        if not self.resources.has_key( to_restype ):
            raise ValueError( "Invalid resource type: %s" % ( to_restype ) )
        to_tuple = ( to_restype, to_resname )
        
        if not self.references.has_key( from_restype ):
            self.references[ from_restype ] = {}
        if not self.references[ from_restype ].has_key( from_resname ):
            self.references[ from_restype ][ from_resname ] = set()
        self.references[ from_restype ][ from_resname ].add( to_tuple )