
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'F082E22554168E6041D10F4ABF4447BC'
    
_lr_action_items = {'STAR':([2,4,5,6,7,8,9,11,12,],[-9,7,-8,7,-5,-6,7,-7,7,]),'SYMBOL':([0,2,3,4,5,6,7,8,9,10,11,12,],[2,-9,2,2,-8,2,-5,-6,2,2,-7,-4,]),'PLUS':([2,4,5,6,7,8,9,11,12,],[-9,8,-8,8,-5,-6,8,-7,-4,]),'LPAREN':([0,2,3,4,5,6,7,8,9,10,11,12,],[3,-9,3,3,-8,3,-5,-6,3,3,-7,-4,]),'RPAREN':([2,3,5,6,7,8,9,11,12,],[-9,5,-8,11,-5,-6,-3,-7,-4,]),'DOT':([2,4,5,6,7,8,9,11,12,],[-9,10,-8,10,-5,-6,10,-7,-4,]),'$end':([0,1,2,4,5,7,8,9,11,12,],[-2,0,-9,-1,-8,-5,-6,-3,-7,-4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,3,4,6,9,10,12,],[4,6,9,9,9,12,9,]),'statement':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','code.py',42),
  ('statement -> <empty>','statement',0,'p_statement_none','code.py',46),
  ('expression -> expression expression','expression',2,'p_expression_concatenation','code.py',50),
  ('expression -> expression DOT expression','expression',3,'p_expression_dot','code.py',53),
  ('expression -> expression STAR','expression',2,'p_expression_star','code.py',57),
  ('expression -> expression PLUS','expression',2,'p_expression_plus','code.py',61),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','code.py',66),
  ('expression -> LPAREN RPAREN','expression',2,'p_expression_empty','code.py',70),
  ('expression -> SYMBOL','expression',1,'p_expression_symbol','code.py',75),
]
