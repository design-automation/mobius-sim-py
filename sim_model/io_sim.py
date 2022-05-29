from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import with_statement
# generators, generator_stop, nested_scopes 
import sys
print("PYTHON Version: ", sys.version_info)
if sys.version_info[0] >= 3:
    unicode = str
from collections import OrderedDict
import json
from sim_model.sim import ENT_TYPE, DATA_TYPE, SIM
# ==================================================================================================
# Functions for importing and exporting models in the SIM file format.
# ==================================================================================================
# ==================================================================================================
# EXPORT
# ==================================================================================================
def export_sim_data(sim_model):
    """Return JSON representing that data in the SIM model.
    
    :return: JSON data.
    """
    # get entities from graph
    posi_ents = sim_model.get_ents(ENT_TYPE.POSIS)
    vert_ents = sim_model.get_ents(ENT_TYPE.VERTS)
    edge_ents = sim_model.get_ents(ENT_TYPE.EDGES)
    wire_ents = sim_model.get_ents(ENT_TYPE.WIRES)
    point_ents = sim_model.get_ents(ENT_TYPE.POINTS)
    pline_ents = sim_model.get_ents(ENT_TYPE.PLINES)
    pgon_ents = sim_model.get_ents(ENT_TYPE.PGONS)
    coll_ents = sim_model.get_ents(ENT_TYPE.COLLS)
    # create maps for entity name -> entity index
    posis_dict = dict( zip(posi_ents, range(len(posi_ents))) )
    verts_dict = dict( zip(vert_ents, range(len(vert_ents))) )
    edges_dict = dict( zip(edge_ents, range(len(edge_ents))) )
    wires_dict = dict( zip(wire_ents, range(len(wire_ents))) )
    points_dict = dict( zip(point_ents, range(len(point_ents))) )
    plines_dict = dict( zip(pline_ents, range(len(pline_ents))) )
    pgons_dict = dict( zip(pgon_ents, range(len(pgon_ents))) )
    colls_dict = dict( zip(coll_ents, range(len(coll_ents))) )
    # create the geometry data
    geometry = {
        'num_posis': sim_model.num_ents(ENT_TYPE.POSIS),
        'points': [],
        'plines': [],
        'pgons': [],
        'coll_points': [],
        'coll_plines': [],
        'coll_pgons':  [],
        'coll_colls': []
    }
    for point_ent in point_ents:
        posi_i = sim_model.get_point_posi(point_ent)
        geometry['points'].append(posis_dict[posi_i])
    for pline_ent in pline_ents:
        posis_i = sim_model.get_pline_posis(pline_ent)
        geometry['plines'].append([posis_dict[posi_i] for posi_i in posis_i])
    for pgon_ent in pgon_ents:
        wires_posis_i = sim_model.get_pgon_posis(pgon_ent)
        geometry['pgons'].append([[posis_dict[posi_i] for posi_i in posis_i] for posis_i in wires_posis_i])
    for coll_ent in coll_ents:
        # points
        coll_points = sim_model.get_ents(ENT_TYPE.POINTS, coll_ent)
        geometry['coll_points'].append([points_dict[point] for point in coll_points])
        # plines
        coll_plines = sim_model.get_ents(ENT_TYPE.PLINES, coll_ent)
        geometry['coll_plines'].append([plines_dict[pline] for pline in coll_plines])
        # pgons
        coll_pgons = sim_model.get_ents(ENT_TYPE.PGONS, coll_ent)
        geometry['coll_pgons'].append([pgons_dict[pgon] for pgon in coll_pgons])
        # colls
        coll_colls = sim_model.get_ents(ENT_TYPE.COLLS, coll_ent)
        geometry['coll_colls'].append([colls_dict[coll] for coll in coll_colls])
    # create the attribute data
    def _attribData(ent_type, ent_dict):
        attribs_data = []
        for att_name in sim_model.get_attribs(ent_type):
            data = dict()
            data['name'] = att_name
            data['data_type'] = sim_model.get_attrib_datatype(ent_type, att_name)
            data['values'] = []
            data['entities'] = []
            for att_val in sim_model.get_attrib_vals(ent_type, att_name):
                data['values'].append(att_val)
                ents = sim_model.query(ent_type, att_name, '==', att_val)
                ents_i = [ent_dict[ent] for ent in ents]
                data['entities'].append(ents_i)
            attribs_data.append(data)
        return attribs_data
    attributes = {
        'posis': _attribData(ENT_TYPE.POSIS, posis_dict),
        'verts': _attribData(ENT_TYPE.VERTS, verts_dict),
        'edges': _attribData(ENT_TYPE.EDGES, edges_dict),
        'wires': _attribData(ENT_TYPE.WIRES, wires_dict),
        'points': _attribData(ENT_TYPE.POINTS, points_dict),
        'plines': _attribData(ENT_TYPE.PLINES, plines_dict),
        'pgons': _attribData(ENT_TYPE.PGONS, pgons_dict),
        'colls': _attribData(ENT_TYPE.COLLS, colls_dict),
        'model': [
            [att_name, sim_model.get_model_attrib_val(att_name)] 
            for att_name in sim_model.get_model_attribs()
        ]
    }
    # create the json
    data = {
        'type': 'SIM',
        'version': '0.1',
        'geometry': geometry,
        'attributes': attributes
    }
    return data
# ----------------------------------------------------------------------------------------------
def export_sim(sim_model):
    """Return a JSON formatted string representing that data in the model.
    
    :return: A JSON string in the SIM format.
    """
    return json.dumps(export_sim_data(sim_model))
# ----------------------------------------------------------------------------------------------
def export_sim_file(sim_model, filepath):
    """Import SIM file.
    
    :return: No value.
    """
    with open(filepath, 'w') as f:
        f.write( json.dumps(sim_model.export_sim_data()) )
# ==================================================================================================
# IMPORT
# ==================================================================================================
def import_sim_data(sim_model, json_data):
    """Import SIM JSON data.
    
    :return: No value.
    """
    # positions
    posis = []
    for i in range(json_data['geometry']['num_posis']):
        posis.append(sim_model.add_posi([0,0,0]))
    # points
    for posi_i in json_data['geometry']['points']:
        sim_model.add_point(posis[posi_i])
    # polylines
    for posis_i in json_data['geometry']['plines']:
        closed = posis_i[0] == posis_i[-1]
        sim_model.add_pline(map(lambda posi_i: posis[posi_i], posis_i), closed)
    # polygons
    for posis_i in json_data['geometry']['pgons']:
        sim_model.add_pgon(map(lambda posi_i: posis[posi_i], posis_i[0]))
        # TODO add holes
    # collections
    num_colls = len(json_data['geometry']['coll_points'])
    for i in range(num_colls):
        coll = sim_model.add_coll()
        for point_i in json_data['geometry']['coll_points'][i]:
            sim_model.add_coll_ent(coll, 'pt' + str(point_i))
        for pline_i in json_data['geometry']['coll_plines'][i]:
            sim_model.add_coll_ent(coll, 'pl' + str(pline_i))
        for pgon_i in json_data['geometry']['coll_pgons'][i]:
            sim_model.add_coll_ent(coll, 'pg' + str(pgon_i))
        for child_coll_i in json_data['geometry']['coll_colls'][i]:
            sim_model.add_coll_ent(coll, 'co' + str(child_coll_i))
    # entity attribs
    ent_types_prefix = [
        [ENT_TYPE.POSIS, 'ps'],
        [ENT_TYPE.VERTS, '_v'],
        [ENT_TYPE.EDGES, '_e'],
        [ENT_TYPE.WIRES, '_w'],
        [ENT_TYPE.POINTS, 'pt'],
        [ENT_TYPE.PLINES, 'pl'],
        [ENT_TYPE.PGONS, 'pg'],
        [ENT_TYPE.COLLS, 'co']
    ]
    for ent_type, ent_prefix in ent_types_prefix:
        for attrib in json_data['attributes'][ent_type]:
            att_name = attrib['name']
            if att_name != 'xyz':
                sim_model.add_attrib(ent_type, att_name, attrib['data_type'])
            for i in range(len(attrib['values'])):
                att_value = attrib['values'][i]
                for ent_i in attrib['entities'][i]:
                    ent = ent_prefix + str(ent_i)
                    sim_model.set_attrib_val(ent, att_name, att_value)
    # model attributes
    for [attrib_name, attrib_val] in json_data['attributes']['model']:
        sim_model.set_model_attrib_val(attrib_name, attrib_val)
# ----------------------------------------------------------------------------------------------
def import_sim(sim_model, json_str):
    """Import SIM string.
    
    :return: No value.
    """
    import_sim_data(sim_model, json.loads(json_str))
# ----------------------------------------------------------------------------------------------
def import_sim_file(sim_model, filepath):
    """Import SIM file.
    
    :return: No value.
    """
    with open(filepath, 'r') as f:
        import_sim_data(sim_model, json.loads(f.read()))
# ==================================================================================================
