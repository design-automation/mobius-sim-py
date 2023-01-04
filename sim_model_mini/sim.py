from __future__ import absolute_import,division,print_function
from collections import OrderedDict
import copy,json
class Graph:
	FWD=0;REV=1
	def __init__(self):self._nodes=OrderedDict();self._edges_reversed=dict();self._edges=dict();self._edges[0]=OrderedDict();self._curr_ssid=0
	def add_node(self,node):
		if node in self._nodes:raise Exception('Node already exists.')
		self._nodes[node]=dict()
	def set_node_prop(self,node,prop_name,prop_value):
		if not node in self._nodes:raise Exception('Node does not exist.')
		self._nodes[node][prop_name]=prop_value
	def get_node_prop(self,node,prop_name):
		if not node in self._nodes:raise Exception('Node does not exist.')
		return self._nodes[node][prop_name]
	def get_node_prop_names(self,node):
		if not node in self._nodes:raise Exception('Node does not exist.')
		return list(self._nodes[node].keys())
	def get_nodes(self):return list(self._nodes.keys())
	def get_nodes_with_out_edge(self,edge_type,ssid=None):
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		return list(self._edges[ssid][edge_type][Graph.FWD].keys())
	def get_nodes_with_in_edge(self,edge_type,ssid=None):
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		return list(self._edges[ssid][edge_type][Graph.REV].keys())
	def has_node(self,node):return node in self._nodes
	def add_edge(self,node0,node1,edge_type,ssid=None):
		if not node0 in self._nodes and node1 in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:
			edges=dict();edges[Graph.FWD]=OrderedDict()
			if self._edges_reversed[edge_type]:edges[Graph.REV]=OrderedDict()
			self._edges.get(ssid)[edge_type]=edges
		edges=self._edges[ssid][edge_type];edge_fwd=self._edges[ssid][edge_type][Graph.FWD]
		if node0 not in edge_fwd:edge_fwd[node0]=OrderedDict()
		edge_fwd[node0][node1]=None
		if self._edges_reversed[edge_type]:
			edge_rev=self._edges[ssid][edge_type][Graph.REV]
			if node1 not in edge_rev:edge_rev[node1]=OrderedDict()
			edge_rev[node1][node0]=None
	def del_edge(self,node0,node1,edge_type,ssid=None):
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		rev=self._edges_reversed[edge_type]
		if edge_type not in self._edges[ssid]:return
		edges=self._edges[ssid][edge_type]
		if node0 is None:
			if not rev:raise Exception('Edge type "'+edge_type+'" does not have reverse edges.')
			if node1 in edges[Graph.REV]:
				for node in edges[Graph.REV][node1]:edges[Graph.FWD][node].pop(node1)
				edges[Graph.REV][node1].clear()
			return
		if node1 is None:
			if node0 in edges[Graph.FWD]:
				if rev:
					for node in edges[Graph.FWD][node0]:edges[Graph.REV][node].pop(node0)
				edges[Graph.FWD][node0].clear()
			return
		if node0 not in self._nodes or node1 not in self._nodes:raise Exception('Node does not exist: '+str(node0)+', '+str(node1)+'.')
		if node0==node1:raise Exception('Nodes cannot be the same.')
		if edge_type not in self._edges[ssid]:return
		if node0 not in edges[Graph.FWD]or node1 not in edges[Graph.FWD][node0]:return
		edges[Graph.FWD][node0].pop(node1)
		if rev:edges[Graph.REV][node1].pop(node0)
	def has_edge(self,node0,node1,edge_type,ssid=None):
		if not node0 in self._nodes and node1 in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:return False
		edges_fwd=self._edges[ssid][edge_type][Graph.FWD]
		if node0 not in edges_fwd:return False
		return node1 in edges_fwd[node0]
	def add_edge_type(self,edge_type,rev,ssid=None):
		if edge_type in self._edges_reversed:raise Exception('Edge type already exists.')
		if ssid is None:ssid=self._curr_ssid
		self._edges_reversed[edge_type]=rev
	def has_edge_type(self,edge_type):return edge_type in self._edges_reversed
	def successors(self,node,edge_type,ssid=None):
		if not node in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:return[]
		edges=self._edges[ssid][edge_type]
		if node not in edges[Graph.FWD]:return[]
		return list(edges[Graph.FWD][node])
	def predecessors(self,node,edge_type,ssid=None):
		if not node in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if not self._edges_reversed[edge_type]:raise Exception('Edge types "'+edge_type+'" does not have reverse edges.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:return[]
		edges=self._edges[ssid][edge_type]
		if node not in edges[Graph.REV]:return[]
		return list(edges[Graph.REV][node])
	def set_successors(self,node0,nodes1,edge_type,ssid=None):
		if node0 not in self._nodes:raise Exception('Node does not exist: '+node0+'.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:
			edges=dict();edges[Graph.FWD]=OrderedDict()
			if self._edges_reversed[edge_type]:edges[Graph.REV]=OrderedDict()
			self._edges[ssid][edge_type]=edges
		edges=self._edges[ssid][edge_type];edges[Graph.FWD][node0].clear()
		for node1 in nodes1:edges[Graph.FWD][node0][node1]=None
	def set_predecessors(self,node1,nodes0,edge_type,ssid=None):
		if node1 not in self._nodes:raise Exception('Node does not exist: '+node1+'.')
		if not self._edges_reversed.get(edge_type):raise Exception('Edge types "'+edge_type+'" does not have reverse edges.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:
			edges=dict();edges[Graph.FWD]=OrderedDict()
			if self._edges_reversed.get(edge_type):edges[Graph.REV]=OrderedDict()
			self._edges[ssid][edge_type]=edges
		edges=self._edges[ssid][edge_type];edges[Graph.REV][node1].clear()
		for node0 in nodes0:edges[Graph.REV][node1][node0]=None
	def degree_in(self,node,edge_type,ssid=None):
		if not node in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if not self._edges_reversed[edge_type]:raise Exception('Edge types "'+edge_type+'" does not have reverse edges.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:return 0
		edges=self._edges[ssid][edge_type]
		if node not in edges[Graph.REV]:return 0
		return len(edges[Graph.REV][node])
	def degree_out(self,node,edge_type,ssid=None):
		if not node in self._nodes:raise Exception('Node does not exist.')
		if not edge_type in self._edges_reversed:raise Exception('Edge type does not exist.')
		if ssid is None:ssid=self._curr_ssid
		if edge_type not in self._edges[ssid]:return 0
		edges=self._edges[ssid][edge_type]
		if node not in edges[Graph.FWD]:return 0
		return len(edges[Graph.FWD][node])
	def degree(self,node,edge_type):return self.degree_in(node,edge_type)+self.degree_out(node,edge_type)
	def new_snapshot(self,ssid=None):
		self._curr_ssid+=1
		if ssid is None:self._edges[self._curr_ssid]=OrderedDict()
		else:self._edges[self._curr_ssid]=copy.deepcopy(self._edges.get(ssid))
		return self._curr_ssid
	def get_active_snapshot(self):return self._curr_ssid
	def set_active_snapshot(self,ssid):
		if not ssid in self._edges:raise Exception('Snapshot ID does not exist.')
		self._curr_ssid=ssid
	def clear_snapshot(self,ssid=None):
		if ssid is None:ssid=self._curr_ssid
		self._edges[self._curr_ssid]=OrderedDict()
	def to_string(self):
		info='\n\n=GRAPH=\n';info+='NODES = '+str(self.get_nodes())+'\n'
		for (ssid,edge_types_map) in self._edges.items():
			info+='SSID = '+str(ssid)+'\n'
			for (edge_type,fr_edges_map) in edge_types_map.items():
				info+='    EDGE TYPE = '+edge_type+', reverse = '+str(self._edges_reversed[edge_type])+'\n'
				if Graph.FWD in fr_edges_map:
					for (start,end) in fr_edges_map[Graph.FWD].items():
						info+='      FWD EDGE: '+start+' -> ';type_end=type(end)
						if type_end is set or type_end is OrderedDict:info+=str(list(end))+'\n'
						else:info+=str(end)+'\n'
					if self._edges_reversed[edge_type]:
						for (start,end) in fr_edges_map[Graph.REV].items():
							info+='      REV EDGE: ';type_end=type(end)
							if type_end is set or type_end is OrderedDict:info+=str(list(end))
							else:info+=end
							info+=' <- '+start+'\n'
		return info
class ENT_TYPE:POSI='ps';VERT='_v';EDGE='_e';WIRE='_w';TRI='_t';POINT='pt';PLINE='pl';PGON='pg';COLL='co';COLL_PRED='cp';COLL_SUCC='cs';MODEL='mo'
class VERT_TYPE:PLINE='pl';PGON='pg';PGON_HOLE='pgh'
class DATA_TYPE:NUM='number';STR='string';BOOL='boolean';LIST='list';DICT='dict'
class COMPARATOR:IS_EQUAL='==';IS_NOT_EQUAL='!=';IS_GREATER_OR_EQUAL='>=';IS_LESS_OR_EQUAL='<=';IS_GREATER='>';IS_LESS='<'
_GR_ENTS_NODE={ENT_TYPE.POSI:'_ents_posis',ENT_TYPE.VERT:'_ents_verts',ENT_TYPE.EDGE:'_ents_edges',ENT_TYPE.WIRE:'_ents_wires',ENT_TYPE.TRI:'_ents_tris',ENT_TYPE.POINT:'_ents_points',ENT_TYPE.PLINE:'_ents_plines',ENT_TYPE.PGON:'_ents_pgons',ENT_TYPE.COLL:'_ents_colls'}
_GR_ATTRIBS_NODE={ENT_TYPE.POSI:'_atts_posis',ENT_TYPE.VERT:'_atts_verts',ENT_TYPE.EDGE:'_atts_edges',ENT_TYPE.WIRE:'_atts_wires',ENT_TYPE.POINT:'_atts_points',ENT_TYPE.PLINE:'_atts_plines',ENT_TYPE.PGON:'_atts_pgons',ENT_TYPE.COLL:'_atts_colls'}
_GR_XYZ_NODE='_att_ps_xyz'
class _GR_EDGE_TYPE:ENT='entity';ATT='attrib';META='meta';TRI='tri'
_ENT_SEQ={ENT_TYPE.POSI:0,ENT_TYPE.VERT:1,ENT_TYPE.EDGE:2,ENT_TYPE.WIRE:3,ENT_TYPE.POINT:4,ENT_TYPE.PLINE:4,ENT_TYPE.PGON:4,ENT_TYPE.COLL:6}
_ENT_SEQ_CO_PT_PO={ENT_TYPE.POSI:0,ENT_TYPE.VERT:1,ENT_TYPE.POINT:2,ENT_TYPE.COLL:6}
_ENT_SEQ_CO_PL_PO={ENT_TYPE.POSI:0,ENT_TYPE.VERT:1,ENT_TYPE.EDGE:2,ENT_TYPE.WIRE:3,ENT_TYPE.PLINE:4,ENT_TYPE.COLL:6}
_ENT_SEQ_CO_PG_PO={ENT_TYPE.POSI:0,ENT_TYPE.VERT:1,ENT_TYPE.EDGE:2,ENT_TYPE.WIRE:3,ENT_TYPE.PGON:4,ENT_TYPE.COLL:6}
_COLL_ENT_TYPES={ENT_TYPE.POINT,ENT_TYPE.PLINE,ENT_TYPE.PGON,ENT_TYPE.COLL}
_OBJ_ENT_TYPES={ENT_TYPE.POINT,ENT_TYPE.PLINE,ENT_TYPE.PGON}
_TOPO_ENT_TYPES={ENT_TYPE.VERT,ENT_TYPE.EDGE,ENT_TYPE.WIRE}
_ALL_ENT_TYPES={ENT_TYPE.POSI,ENT_TYPE.VERT,ENT_TYPE.EDGE,ENT_TYPE.WIRE,ENT_TYPE.POINT,ENT_TYPE.PLINE,ENT_TYPE.PGON,ENT_TYPE.COLL}
class SIM:
	def __init__(self):
		self.graph=Graph();self.graph.add_edge_type(_GR_EDGE_TYPE.ENT,True);self.graph.add_edge_type(_GR_EDGE_TYPE.ATT,True);self.graph.add_edge_type(_GR_EDGE_TYPE.META,False);self.graph.add_edge_type(_GR_EDGE_TYPE.TRI,True)
		for ent_type in [ENT_TYPE.POSI,ENT_TYPE.VERT,ENT_TYPE.EDGE,ENT_TYPE.WIRE,ENT_TYPE.TRI,ENT_TYPE.POINT,ENT_TYPE.PLINE,ENT_TYPE.PGON,ENT_TYPE.COLL]:self.graph.add_node(_GR_ENTS_NODE[ent_type])
		for ent_type in [ENT_TYPE.POSI,ENT_TYPE.VERT,ENT_TYPE.EDGE,ENT_TYPE.WIRE,ENT_TYPE.POINT,ENT_TYPE.PLINE,ENT_TYPE.PGON,ENT_TYPE.COLL]:self.graph.add_node(_GR_ATTRIBS_NODE[ent_type])
		self._graph_add_attrib(ENT_TYPE.POSI,'xyz',DATA_TYPE.LIST);self.model_attribs=dict()
	def add_posi(self,xyz=None):
		posi=self._graph_add_ent(ENT_TYPE.POSI)
		if xyz is not None:self.set_posi_coords(posi,xyz)
		return posi
	def add_point(self,posi):vert=self._graph_add_ent(ENT_TYPE.VERT);point=self._graph_add_ent(ENT_TYPE.POINT);self.graph.add_edge(vert,posi,_GR_EDGE_TYPE.ENT);self.graph.add_edge(point,vert,_GR_EDGE_TYPE.ENT);return point
	def add_pline(self,posis,closed):
		if len(posis)<2:raise Exception('Too few positions for polyline.')
		pline=self._graph_add_ent(ENT_TYPE.PLINE);wire=self._graph_add_ent(ENT_TYPE.WIRE);self.graph.add_edge(pline,wire,_GR_EDGE_TYPE.ENT);self._add_edge_seq(posis,closed,VERT_TYPE.PLINE,wire);return pline
	def add_pgon(self,posis):
		posis=posis if type(posis[0])is list else[posis]
		if len(posis[0])<3:raise Exception('Too few positions for polygon.')
		pgon=self._graph_add_ent(ENT_TYPE.PGON);wire=self._graph_add_ent(ENT_TYPE.WIRE);self.graph.add_edge(pgon,wire,_GR_EDGE_TYPE.ENT);self._add_edge_seq(posis[0],True,VERT_TYPE.PGON,wire)
		for i in range(1,len(posis)):self.add_pgon_hole(pgon,posis[i])
		return pgon
	def add_pgon_hole(self,pgon,posis):
		if len(posis)<3:raise Exception('Too few positions for polygon hole.')
		wire=self._graph_add_ent(ENT_TYPE.WIRE);self.graph.add_edge(pgon,wire,_GR_EDGE_TYPE.ENT);self._add_edge_seq(posis,True,VERT_TYPE.PGON_HOLE,wire);return wire
	def _add_edge_seq(self,posis,closed,vert_type,parent):
		edges=[];v0=None;v1=None;v_start=self._graph_add_ent(ENT_TYPE.VERT);self.graph.set_node_prop(v_start,'vert_type',vert_type);self.graph.add_edge(v_start,posis[0],_GR_EDGE_TYPE.ENT);v0=v_start
		for i in range(1,len(posis)):v1=self._graph_add_ent(ENT_TYPE.VERT);self.graph.set_node_prop(v1,'vert_type',vert_type);self.graph.add_edge(v1,posis[i],_GR_EDGE_TYPE.ENT);edge=self._graph_add_ent(ENT_TYPE.EDGE);self.graph.add_edge(parent,edge,_GR_EDGE_TYPE.ENT);self.graph.add_edge(edge,v0,_GR_EDGE_TYPE.ENT);self.graph.add_edge(edge,v1,_GR_EDGE_TYPE.ENT);v0=v1;edges.append(edge)
		if closed:last_edge=self._graph_add_ent(ENT_TYPE.EDGE);self.graph.add_edge(parent,last_edge,_GR_EDGE_TYPE.ENT);self.graph.add_edge(last_edge,v1,_GR_EDGE_TYPE.ENT);self.graph.add_edge(last_edge,v_start,_GR_EDGE_TYPE.ENT);self.graph.set_predecessors(v_start,[last_edge,edges[0]],_GR_EDGE_TYPE.ENT)
	def triangulate_pgon(self,pgon):raise Exception('Not implements.')
	def copy_ents(self,ents,vec=None):raise Exception('Not implements.')
	def clone_ents(self,ents):raise Exception('Not implements.')
	def add_coll(self):return self._graph_add_ent(ENT_TYPE.COLL)
	def add_coll_ent(self,coll,ent):
		ent_type=self.graph.get_node_prop(ent,'ent_type')
		if ent_type not in _COLL_ENT_TYPES:raise Exception('Invalid entitiy for collections.')
		self.graph.add_edge(coll,ent,_GR_EDGE_TYPE.ENT)
	def rem_coll_ent(self,coll,ent):self.graph.del_edge(coll,ent,_GR_EDGE_TYPE.ENT)
	def add_attrib(self,ent_type,att_name,att_data_type):
		att=self._graph_attrib_node_name(ent_type,att_name)
		if not self.graph.has_node(att):self._graph_add_attrib(ent_type,att_name,att_data_type)
		elif self.graph.get_node_prop(att,'data_type')!=att_data_type:raise Exception('Attribute already exists with different data type')
	def has_attrib(self,ent_type,att_name):att=self._graph_attrib_node_name(ent_type,att_name);return self.graph.has_node(att)
	def get_attribs(self,ent_type):return map(lambda att:self.graph.get_node_prop(att,'name'),self.graph.successors(_GR_ATTRIBS_NODE[ent_type],_GR_EDGE_TYPE.META))
	def set_attrib_val(self,ent,att_name,att_value):
		ent_type=self.graph.get_node_prop(ent,'ent_type');att_node=self._graph_attrib_node_name(ent_type,att_name)
		if ent_type!=self.graph.get_node_prop(att_node,'ent_type'):raise Exception('Entity and attribute have different types.')
		data_type=self._check_type(att_value)
		if self.graph.get_node_prop(att_node,'data_type')!=data_type:raise Exception('Attribute value has the wrong data type: '+str(att_value)+'The data type is a "'+data_type+'". '+'The data type should be a "'+self.graph.get_node_prop(att_node,'data_type')+'".')
		att_val_node=self._graph_attrib_val_node_name(att_value,att_node)
		if not self.graph.has_node(att_val_node):self.graph.add_node(att_val_node);self.graph.set_node_prop(att_val_node,'value',att_value)
		self.graph.add_edge(att_val_node,att_node,_GR_EDGE_TYPE.ATT);self.graph.del_edge(ent,None,att_node);self.graph.add_edge(ent,att_val_node,att_node)
	def get_attrib_val(self,ent,att_name):
		ent_type=self.graph.get_node_prop(ent,'ent_type');att_node=self._graph_attrib_node_name(ent_type,att_name);succs=self.graph.successors(ent,att_node)
		if len(succs)==0:return None
		return self.graph.get_node_prop(succs[0],'value')
	def del_attrib_val(self,ent,att_name):
		ent_type=self.graph.get_node_prop(ent,'ent_type');att_node=self._graph_attrib_node_name(ent_type,att_name);succs=self.graph.successors(ent,att_node)
		if len(succs)==0:return
		self.graph.del_edge(ent,succs[0],att_node)
	def get_attrib_vals(self,ent_type,att_name):
		att_node=self._graph_attrib_node_name(ent_type,att_name);att_val_nodes=self.graph.predecessors(att_node,_GR_EDGE_TYPE.ATT);values=[]
		for att_val_node in att_val_nodes:values.append(self.graph.get_node_prop(att_val_node,'value'))
		return values
	def get_attrib_datatype(self,ent_type,att_name):att_node=self._graph_attrib_node_name(ent_type,att_name);return self.graph.get_node_prop(att_node,'data_type')
	def rename_attrib(self,ent_type,att_name,new_name):
		old_att_node=self._graph_attrib_node_name(ent_type,att_name);att_data_type=self.graph.get_node_prop(old_att_node,'data_type');new_att_node=self._graph_add_attrib(ent_type,new_name,att_data_type)
		for pred in self.graph.predecessors(old_att_node,_GR_EDGE_TYPE.ATT):self.graph.del_edge(pred,old_att_node,_GR_EDGE_TYPE.ATT);self.graph.add_edge(pred,new_att_node,_GR_EDGE_TYPE.ATT)
	def has_model_attrib(self,att_name):return att_name in self.model_attribs
	def set_model_attrib_val(self,att_name,att_value):self.model_attribs[att_name]=att_value
	def get_model_attrib_val(self,att_name):return self.model_attribs[att_name]
	def del_model_attrib_val(self,att_name):del self.model_attribs[att_name]
	def get_model_attribs(self):return self.model_attribs.keys()
	def num_ents(self,ent_type):return self.graph.degree_out(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META)
	def get_ents(self,target_ent_type,source_ents=None):
		if source_ents==None:return self.graph.successors(_GR_ENTS_NODE[target_ent_type],_GR_EDGE_TYPE.META)
		if not type(source_ents)is list:return self._nav(target_ent_type,source_ents)
		ents_set=OrderedDict()
		for source_ent in source_ents:
			for target_ent in self._nav(target_ent_type,source_ent):ents_set[target_ent]=None
		return list(ents_set.keys())
	def _get_ent_seq(self,target_ent_type,source_ent_type):
		if target_ent_type==ENT_TYPE.POINT or source_ent_type==ENT_TYPE.POINT:return _ENT_SEQ_CO_PT_PO
		elif target_ent_type==ENT_TYPE.PLINE or source_ent_type==ENT_TYPE.PLINE:return _ENT_SEQ_CO_PL_PO
		elif target_ent_type==ENT_TYPE.PGON or source_ent_type==ENT_TYPE.PGON:return _ENT_SEQ_CO_PG_PO
		return _ENT_SEQ
	def _nav(self,target_ent_type,source_ent):
		source_ent_type=self.graph.get_node_prop(source_ent,'ent_type');ent_seq=self._get_ent_seq(target_ent_type,source_ent_type)
		if source_ent_type==target_ent_type:
			if source_ent_type==ENT_TYPE.COLL:return[]
			return[source_ent]
		dist=ent_seq[source_ent_type]-ent_seq[target_ent_type]
		if dist==1:return self.graph.successors(source_ent,_GR_EDGE_TYPE.ENT)
		if dist==-1:return self.graph.predecessors(source_ent,_GR_EDGE_TYPE.ENT)
		navigate=self.graph.successors if dist>0 else self.graph.predecessors;ents=[source_ent];target_ents_set=OrderedDict()
		while ents:
			ent_set=OrderedDict()
			for ent in ents:
				for target_ent in navigate(ent,_GR_EDGE_TYPE.ENT):
					this_ent_type=self.graph.get_node_prop(target_ent,'ent_type')
					if this_ent_type==target_ent_type:target_ents_set[target_ent]=None
					elif this_ent_type in ent_seq:
						if dist>0 and ent_seq[this_ent_type]>ent_seq[target_ent_type]:ent_set[target_ent]=None
						elif dist<0 and ent_seq[this_ent_type]<ent_seq[target_ent_type]:ent_set[target_ent]=None
			ents=ent_set.keys()
		return list(target_ents_set.keys())
	def get_ent_posis(self,ent):
		ent_type=self.graph.get_node_prop(ent,'ent_type')
		if ent_type==ENT_TYPE.POSI:return ent
		elif ent_type==ENT_TYPE.VERT:return self.graph.successors(ent,_GR_EDGE_TYPE.ENT)[0]
		elif ent_type==ENT_TYPE.EDGE:verts=self.graph.successors(ent,_GR_EDGE_TYPE.ENT);return[self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0]for vert in verts]
		elif ent_type==ENT_TYPE.WIRE:edges=self.graph.successors(ent,_GR_EDGE_TYPE.ENT);verts=[self.graph.successors(edge,_GR_EDGE_TYPE.ENT)[0]for edge in edges];posis=[self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0]for vert in verts];last_vert=self.graph.successors(edges[-1],_GR_EDGE_TYPE.ENT)[1];last_posi=self.graph.successors(last_vert,_GR_EDGE_TYPE.ENT)[0];posis.append(last_posi);return posis
		elif ent_type==ENT_TYPE.POINT:vert=self.graph.successors(ent,_GR_EDGE_TYPE.ENT)[0];return self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0]
		elif ent_type==ENT_TYPE.PLINE:wire=self.graph.successors(ent,_GR_EDGE_TYPE.ENT)[0];edges=self.graph.successors(wire,_GR_EDGE_TYPE.ENT);verts=[self.graph.successors(edge,_GR_EDGE_TYPE.ENT)[0]for edge in edges];posis=[self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0]for vert in verts];last_vert=self.graph.successors(edges[-1],_GR_EDGE_TYPE.ENT)[1];last_posi=self.graph.successors(last_vert,_GR_EDGE_TYPE.ENT)[0];posis.append(last_posi);return posis
		elif ent_type==ENT_TYPE.PGON:
			posis=[]
			for wire in self.graph.successors(ent,_GR_EDGE_TYPE.ENT):edges=self.graph.successors(wire,_GR_EDGE_TYPE.ENT);verts=[self.graph.successors(edge,_GR_EDGE_TYPE.ENT)[0]for edge in edges];wire_posis=[self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0]for vert in verts];posis.append(wire_posis)
			return posis
		elif ent_type==ENT_TYPE.COLL:raise Exception('Not implemented')
	def get_vert_coords(self,vert):posi=self.graph.successors(vert,_GR_EDGE_TYPE.ENT)[0];att_val_node=self.graph.successors(posi,_GR_XYZ_NODE)[0];return self.graph.get_node_prop(att_val_node,'value')
	def get_posi_coords(self,posi):att_val_node=self.graph.successors(posi,_GR_XYZ_NODE)[0];return self.graph.get_node_prop(att_val_node,'value')
	def set_posi_coords(self,posi,xyz):
		att_val_node=self._graph_attrib_val_node_name(xyz,_GR_XYZ_NODE)
		if not self.graph.has_node(att_val_node):self.graph.add_node(att_val_node);self.graph.set_node_prop(att_val_node,'value',xyz)
		self.graph.add_edge(att_val_node,_GR_XYZ_NODE,_GR_EDGE_TYPE.ATT);self.graph.del_edge(posi,None,_GR_XYZ_NODE);self.graph.add_edge(posi,att_val_node,_GR_XYZ_NODE);return att_val_node
	def is_pline_closed(self,pline):edges=self.graph.successors(self.graph.successors(pline,_GR_EDGE_TYPE.ENT)[0],_GR_EDGE_TYPE.ENT);start=self.graph.successors(self.graph.successors(edges[0],_GR_EDGE_TYPE.ENT)[0],_GR_EDGE_TYPE.ENT);end=self.graph.successors(self.graph.successors(edges[-1],_GR_EDGE_TYPE.ENT)[1],_GR_EDGE_TYPE.ENT);return start==end
	def query(self,ent_type,att_name,comparator,att_val):
		att_node=self._graph_attrib_node_name(ent_type,att_name)
		if not self.graph.has_node(att_node):raise Exception("The attribute does not exist: '"+att_name+"'.")
		if comparator=='=='and att_val==None:set_with_val=set(self.graph.get_nodes_with_out_edge(att_node));set_all=set(self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META));return list(set_all-set_with_val)
		if comparator=='!='and att_val==None:return self.graph.get_nodes_with_out_edge(att_node)
		if comparator=='==':
			att_val_node=self._graph_attrib_val_node_name(att_val,att_node)
			if not self.graph.has_node(att_val_node):return[]
			return self.graph.predecessors(att_val_node,att_node)
		if comparator=='!=':
			att_val_node=self._graph_attrib_val_node_name(att_val,att_node)
			if not self.graph.has_node(att_val_node):return self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META)
			ents_equal=self.graph.predecessors(att_val_node,att_node)
			if len(ents_equal)==0:return self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META)
			set_equal=set(ents_equal);set_all=set(self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META));return list(set_all-set_equal)
		data_type=self.graph.get_node_prop(att_node,'data_type')
		if data_type!=DATA_TYPE.NUM:raise Exception("The '"+comparator+"' comparator cannot be used with attributes of type '"+data_type+"'.")
		result=[]
		if comparator=='<':
			result=[]
			for ent in self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META):
				succs=self.graph.successors(ent,att_node)
				if len(succs)!=0 and self.graph.get_node_prop(succs[0],'value')<att_val:result.append(ent)
		if comparator=='<=':
			result=[]
			for ent in self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META):
				succs=self.graph.successors(ent,att_node)
				if len(succs)!=0 and self.graph.get_node_prop(succs[0],'value')<=att_val:result.append(ent)
		if comparator=='>':
			result=[]
			for ent in self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META):
				succs=self.graph.successors(ent,att_node)
				if len(succs)!=0 and self.graph.get_node_prop(succs[0],'value')>att_val:result.append(ent)
		if comparator=='>=':
			result=[]
			for ent in self.graph.successors(_GR_ENTS_NODE[ent_type],_GR_EDGE_TYPE.META):
				succs=self.graph.successors(ent,att_node)
				if len(succs)!=0 and self.graph.get_node_prop(succs[0],'value')>=att_val:result.append(ent)
		return result
	def _graph_attrib_node_name(self,ent_type,att_name):return'_att_'+ent_type+'_'+att_name
	def _graph_attrib_val_node_name(self,att_val,att_node):
		data_type=self.graph.get_node_prop(att_node,'data_type')
		if data_type==DATA_TYPE.NUM or data_type==DATA_TYPE.STR:return att_val
		return str(att_val)
	def _graph_add_ent(self,ent_type):ent_type_n=_GR_ENTS_NODE[ent_type];ent_i=self.graph.degree_out(ent_type_n,edge_type=_GR_EDGE_TYPE.META);ent=ent_type+str(ent_i);self.graph.add_node(ent);self.graph.set_node_prop(ent,'ent_type',ent_type);self.graph.add_edge(ent_type_n,ent,_GR_EDGE_TYPE.META);return ent
	def _graph_add_attrib(self,ent_type,name,data_type):att_node=self._graph_attrib_node_name(ent_type,name);self.graph.add_node(att_node);self.graph.set_node_prop(att_node,'ent_type',ent_type);self.graph.set_node_prop(att_node,'name',name);self.graph.set_node_prop(att_node,'data_type',data_type);self.graph.add_edge(_GR_ATTRIBS_NODE[ent_type],att_node,_GR_EDGE_TYPE.META);self.graph.add_edge_type(att_node,rev=True);return att_node
	def _graph_add_attrib_val(self,att_node,att_val):
		att_val_node=self._graph_attrib_val_node_name(att_val,att_node)
		if not self.graph.has_node(att_val_node):self.graph.add_node(att_val_node);self.graph.set_node_prop(att_val_node,'value',att_val);self.graph.add_edge(att_val_node,att_node,_GR_EDGE_TYPE.ATT)
		return att_val_node
	def _check_type(self,value):
		val_type=type(value)
		if val_type==int or val_type==float:return DATA_TYPE.NUM
		if val_type==str or val_type==unicode:return DATA_TYPE.STR
		if val_type==bool:return DATA_TYPE.BOOL
		if val_type==list:return DATA_TYPE.LIST
		if val_type==dict:return DATA_TYPE.DICT
		raise Exception('Data type is not recognised:',str(value),type(value))
	def to_string(self):return self.graph.to_string()
def export_sim_data(sim_model):
	posi_ents=sim_model.get_ents(ENT_TYPE.POSI);vert_ents=sim_model.get_ents(ENT_TYPE.VERT);edge_ents=sim_model.get_ents(ENT_TYPE.EDGE);wire_ents=sim_model.get_ents(ENT_TYPE.WIRE);point_ents=sim_model.get_ents(ENT_TYPE.POINT);pline_ents=sim_model.get_ents(ENT_TYPE.PLINE);pgon_ents=sim_model.get_ents(ENT_TYPE.PGON);coll_ents=sim_model.get_ents(ENT_TYPE.COLL);posis_dict=dict(zip(posi_ents,range(len(posi_ents))));verts_dict=dict(zip(vert_ents,range(len(vert_ents))));edges_dict=dict(zip(edge_ents,range(len(edge_ents))));wires_dict=dict(zip(wire_ents,range(len(wire_ents))));points_dict=dict(zip(point_ents,range(len(point_ents))));plines_dict=dict(zip(pline_ents,range(len(pline_ents))));pgons_dict=dict(zip(pgon_ents,range(len(pgon_ents))));colls_dict=dict(zip(coll_ents,range(len(coll_ents))));geometry={'num_posis':sim_model.num_ents(ENT_TYPE.POSI),'points':[],'plines':[],'pgons':[],'coll_points':[],'coll_plines':[],'coll_pgons':[],'coll_colls':[]}
	for point_ent in point_ents:posi_i=sim_model.get_ent_posis(point_ent);geometry['points'].append(posis_dict[posi_i])
	for pline_ent in pline_ents:posis_i=sim_model.get_ent_posis(pline_ent);geometry['plines'].append([posis_dict[posi_i]for posi_i in posis_i])
	for pgon_ent in pgon_ents:wires_posis_i=sim_model.get_ent_posis(pgon_ent);geometry['pgons'].append([[posis_dict[posi_i]for posi_i in posis_i]for posis_i in wires_posis_i])
	for coll_ent in coll_ents:coll_points=sim_model.get_ents(ENT_TYPE.POINT,coll_ent);geometry['coll_points'].append([points_dict[point]for point in coll_points]);coll_plines=sim_model.get_ents(ENT_TYPE.PLINE,coll_ent);geometry['coll_plines'].append([plines_dict[pline]for pline in coll_plines]);coll_pgons=sim_model.get_ents(ENT_TYPE.PGON,coll_ent);geometry['coll_pgons'].append([pgons_dict[pgon]for pgon in coll_pgons]);coll_colls=sim_model.get_ents(ENT_TYPE.COLL,coll_ent);geometry['coll_colls'].append([colls_dict[coll]for coll in coll_colls])
	def _attribData(ent_type,ent_dict):
		attribs_data=[]
		for att_name in sim_model.get_attribs(ent_type):
			data=dict();data['name']=att_name;data['data_type']=sim_model.get_attrib_datatype(ent_type,att_name);data['values']=[];data['entities']=[]
			for att_val in sim_model.get_attrib_vals(ent_type,att_name):data['values'].append(att_val);ents=sim_model.query(ent_type,att_name,'==',att_val);ents_i=[ent_dict[ent]for ent in ents];data['entities'].append(ents_i)
			attribs_data.append(data)
		return attribs_data
	attributes={'posis':_attribData(ENT_TYPE.POSI,posis_dict),'verts':_attribData(ENT_TYPE.VERT,verts_dict),'edges':_attribData(ENT_TYPE.EDGE,edges_dict),'wires':_attribData(ENT_TYPE.WIRE,wires_dict),'points':_attribData(ENT_TYPE.POINT,points_dict),'plines':_attribData(ENT_TYPE.PLINE,plines_dict),'pgons':_attribData(ENT_TYPE.PGON,pgons_dict),'colls':_attribData(ENT_TYPE.COLL,colls_dict),'model':[[att_name,sim_model.get_model_attrib_val(att_name)]for att_name in sim_model.get_model_attribs()]};data={'type':'SIM','version':'0.1','geometry':geometry,'attributes':attributes};return data
def export_sim(sim_model):return json.dumps(export_sim_data(sim_model))
def export_sim_file(sim_model,filepath):
	with open(filepath,'w')as f:f.write(json.dumps(export_sim_data(sim_model)))
def import_sim_data(sim_model,json_data):
	posis=[]
	for i in range(json_data['geometry']['num_posis']):posis.append(sim_model.add_posi([0,0,0]))
	for posi_i in json_data['geometry']['points']:sim_model.add_point(posis[posi_i])
	for posis_i in json_data['geometry']['plines']:closed=posis_i[0]==posis_i[-1];sim_model.add_pline(map(lambda posi_i:posis[posi_i],posis_i),closed)
	for posi_lists_i in json_data['geometry']['pgons']:
		boundary=map(lambda posi_i:posis[posi_i],posi_lists_i[0]);pgon=sim_model.add_pgon(boundary)
		for hole_posis_i in posi_lists_i[1:]:sim_model.add_pgon_hole(pgon,map(lambda posi_i:posis[posi_i],hole_posis_i))
	num_colls=len(json_data['geometry']['coll_points'])
	for i in range(num_colls):
		coll=sim_model.add_coll()
		for point_i in json_data['geometry']['coll_points'][i]:sim_model.add_coll_ent(coll,'pt'+str(point_i))
		for pline_i in json_data['geometry']['coll_plines'][i]:sim_model.add_coll_ent(coll,'pl'+str(pline_i))
		for pgon_i in json_data['geometry']['coll_pgons'][i]:sim_model.add_coll_ent(coll,'pg'+str(pgon_i))
		for child_coll_i in json_data['geometry']['coll_colls'][i]:sim_model.add_coll_ent(coll,'co'+str(child_coll_i))
	ent_type_strs=[['posis',ENT_TYPE.POSI],['verts',ENT_TYPE.VERT],['edges',ENT_TYPE.EDGE],['wires',ENT_TYPE.WIRE],['points',ENT_TYPE.POINT],['plines',ENT_TYPE.PLINE],['pgons',ENT_TYPE.PGON],['colls',ENT_TYPE.COLL]]
	for (sim_ent_type,ent_type) in ent_type_strs:
		for attrib in json_data['attributes'][sim_ent_type]:
			att_name=attrib['name']
			if sim_model.has_attrib(ent_type,att_name):
				if attrib['data_type']!=sim_model.get_attrib_datatype(ent_type,att_name):att_name=att_name+'_'+attrib['data_type']
			else:sim_model.add_attrib(ent_type,att_name,attrib['data_type'])
			for i in range(len(attrib['values'])):
				att_value=attrib['values'][i]
				for ent_i in attrib['entities'][i]:ent=ent_type+str(ent_i);sim_model.set_attrib_val(ent,att_name,att_value)
	for [attrib_name,attrib_val] in json_data['attributes']['model']:sim_model.set_model_attrib_val(attrib_name,attrib_val)
def import_sim(sim_model,json_str):import_sim_data(sim_model,json.loads(json_str))
def import_sim_file(sim_model,filepath):
	with open(filepath,'r')as f:import_sim_data(sim_model,json.loads(f.read()))