from xmlrpc.client import Boolean
from engine.ast import ColRef, TableInfo, View, ast_node, Context
from engine.utils import base62uuid
from engine.expr import expr

class scan(ast_node):
    name = 'scan'
    def __init__(self, parent: "ast_node", node, size = None, context: Context = None):
        self.type = type
        self.size = size
        super().__init__(parent, node, context)
    def init(self, _):
        self.datasource = self.context.datasource
        self.start = ''
        self.body = ''
        self.end = '}'
        self.filter = None
        scan_vars = set(s.it_var for s in self.context.scans)
        self.it_ver = 'i' + base62uuid(2)
        while(self.it_ver in scan_vars):
            self.it_ver = 'i' + base62uuid(6)
        self.parent.context.scans.append(self)
    def produce(self, node):
        if type(node) is ColRef:
            if self.size is None:
                self.start += f'for (auto& {self.it_ver} : {node.reference()}) {{\n'
            else:
                self.start += f"for (uint32_t {self.it_ver} = 0; {self.it_ver} < {node.reference()}.size; ++{self.it_ver}){{\\n"
        elif type(node) is str:
            self.start+= f'for(auto& {self.it_ver} : {node}) {{\n'
        else:
            self.start += f"for (uint32_t {self.it_ver} = 0; {self.it_ver} < {self.size}; ++{self.it_ver}){{\n"
            
    def add(self, stmt):
        self.body+=stmt + '\n'
    def finalize(self):
        self.context.remove_scan(self, self.start + self.body + self.end)
        
class filter(ast_node):
    name = 'filter'
    def __init__(self, parent: "ast_node", node, materialize = False, context = None):
        self.materialize = materialize
        super().__init__(parent, node, context)
    def init(self, _):
        self.datasource = self.context.datasource
        self.view = View(self.context, self.datasource)
        self.value = None
        
    def spawn(self, node):
        # TODO: deal with subqueries
        return super().spawn(node)
    def __materialize__(self):
        if self.materialize:
            cols = [] if self.datasource is None else self.datasource.columns
            self.output = TableInfo('tn'+base62uuid(6), cols, self.context)
            self.output.construct()
            if type(self.value) is View: # cond filtered on tables.
                self.emit(f'{self.value.name}:&{self.value.name}')
                for o, c in zip(self.output.columns,self.value.table.columns):
                    self.emit(f'{o.cname}:{c.cname}[{self.value.name}]')
            elif self.value is not None: # cond is scalar
                tmpVar = 't'+base62uuid(7)
                self.emit(f'{tmpVar}:{self.value}')
                for o, c in zip(self.output.columns, self.datasource.columns):
                    self.emit(f'{o.cname}:$[{tmpVar};{c.cname};()]')
                
    def consume(self, node):
        # TODO: optimizations after converting expr to cnf
        if type(node) is bool and node and self.materialize:
            self.output = self.context.datasource if node else None
            self.value = '1' if node else '0'
        else:
            if type(node) is dict:
                def short_circuit(op, idx, inv = True):
                    v = filter(self, node[op][idx]).value
                    inv_filter = lambda x: not x if inv else x
                    if type(v) is bool and inv_filter(v):
                        self.value = inv_filter(v)
                        self.__materialize__()
                        return None
                    return v
                def binary(l, r, _ty = '&'):
                    if type(l) is bool:
                        self.value = r
                    elif type(r) is bool:
                        self.value = l
                    elif type(l) is View:
                        if type(r) is View:
                            self.emit(f"{l.name}: {l.name} {_ty} {r.name if type(r) is View else f'({r})'}")
                            self.value = l
                    elif type(l) is str:
                        if type(r) is str:
                            self.value = f'({l}){_ty}({r})'
                        else:
                            self.emit(f'{r.name}:{r.name} {_ty} ({l})')
                            self.value = r
                if 'and' in node:
                    l = short_circuit('and', 0)
                    if l is not None:
                        r = short_circuit('and', 1)
                        if r is not None:                
                            binary(l, r)
                    
                elif 'or' in node:
                    l = short_circuit('or', 0, False)
                    if l is not None:
                        r = short_circuit('or', 1, False)
                        if r is not None:                
                            binary(l, r, '|')
                    
                elif 'not' in node:
                    v = filter(self, node['not']).value
                    if type(v) is bool:
                        self.value = not v
                        self.__materialize__()
                    elif type(v) is View:
                        if len(v.table.columns) > 0:
                            all_rows = View(self.context, v.table)
                            self.emit(f'{all_rows.name}:(#{v.table.columns[0].cname})#1')
                            self.emit(f'{v.name}:{all_rows.name}-{v.name}')
                            self.value = v
                    else:
                        self.value = '~(' + v + ')'
                    # TODO: arithmetic ops connecting logical ops.
                else:
                    e = expr(self, node)
                    if e.isvector:
                        v = View(self.context, self.datasource)
                        v.construct()
                        self.emit(f'{v.name}:{e.cexpr}')
                        self.value = v
                    else:
                        self.value = e.cexpr
            self.__materialize__()        

        print(node)
    