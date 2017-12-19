# Verifica se duas edges se cruzam e inseri um vertex nesse ponto

import bpy, bmesh
from mathutils import Vector

globCo = lambda co, o: o.matrix_world * co

def find_intersection( edges, o ):
    # Calcula posições globais dos vértices das arestas
    p1, p2 = [ globCo( v.co, o ) for v in edges[0].verts ]
    p3, p4 = [ globCo( v.co, o ) for v in edges[1].verts ]

    v1 = p2 - p1 # Aresta 1
    v2 = p4 - p3 # Aresta 2

    # Calcula a interseção 
    # Baseado na equação: (x,y,z) = p0 + t * lineVec
    numer = v2.y * ( p3.x - p1.x ) + v2.x * ( p1.y - p3.y )
    denom = v1.x * v2.y - v1.y * v2.x
    t1    = numer / denom

    co = Vector( [ getattr( p1, i ) + t1 * getattr( v1, i ) for i in 'xyz' ] )

    bpy.context.scene.cursor_location = co

    return co

o  = bpy.context.object

if o.mode == 'EDIT':
    bm    = bmesh.from_edit_mesh( o.data )
    edges = [ e for e in bm.edges if e.select ]

    if len( edges ) == 2:
        co = find_intersection( edges, o )

        # Divide as arestas e adiciona novos vértices na arestas criadas
        for e in edges:
            p1, p2 = [ globCo( v.co, o ) for v in e.verts ]
            fac = ( co - p1 ).length / ( p2 - p1 ).length
            bmesh.utils.edge_split( e, e.verts[0], fac )

# Remove vértices duplicados
bpy.ops.mesh.select_mode( type = 'VERT' )
bpy.ops.mesh.select_all( action = 'SELECT' )
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.select_all( action = 'DESELECT' )
bpy.ops.mesh.select_mode( type = 'EDGE' )