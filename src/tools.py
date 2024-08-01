from enum import Enum as enum
from enum import auto
from dataclasses import dataclass as struct

DEBUG=True#False

@struct
class Locale:
 line:int
 char:int 
 def formate(self)->str:
  return f'{self.line}:{self.char}'


class tokentype(enum):
 BOF        =auto()
 EOF        =auto()
 none       =auto()
 word       =auto()
 numder     =auto()
 syntax     =auto()
 opator     =auto()
 string     =auto()
 keyword    =auto()
 statment   =auto()
 expression =auto()
 block      =auto()
 linend     =auto()

@struct
class token:
 type:tokentype
 lexeme:any
 locale:Locale
 def __repr__(self)->str:
  return f'<type:{self.type.__str__()[10:]},lexeme:{self.lexeme.__repr__()}>'

def tokensToString(inp:list[token])->str:
 out=''
 for v in inp:
  out+=v.lexeme
 return out

class funcType(enum):
 function =auto()
 operator =auto()
@struct
class Signature:
 beginSignature:list
 endSignature:list

@struct
class IF:
 statment:list[token]
 block:list[token]
 elifStatment:list[list[token]]
 elifBlock:list[list[token]]
 elseBlock:list[token]
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f"""if {self.statment}:\n{self.block}""", [f'elif {self.elifStatment[i]}:\n{self.elifBlock[i]}' for i in range(len(self.elifStatment))],f'else:\n{self.elseBlock}' if self.elseBlock!=[] else '',sep='\n')
@struct
class FN:
 name:str
 type:funcType
 loacalVars:dict[str]
 signature:Signature
 body:list[token]
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'fn {self.name}{self.loacalVars}{self.signature.endSignature}:\n{self.body}')
@struct
class VAR:
 name:str
 type:str|int
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'{self.name}:{self.type}')
@struct
class TYPE:
 name:str
 localsVars:dict
 size:int
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'type {self.name}:{self.localsVars}')
@struct
class FNCALL:
 function:str
 args:list[list[token]]
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'{self.function}{self.args}')
@struct
class DOTACSESING:
 name:token
 method:token
 def __repr__(self)->str:
  return f'{type(self).__name__}'#f'{self.name.lexeme}.{self.method.lexeme}'
 def print(self):
  print(f'{self.name}.{self.method}')
@struct
class AST:
 value:any=None
 left:any=None
 richt:any=None
 def __repr__(self)->str:
  return f'({self.left}{self.value.lexeme}{self.richt})'
 def add(self,value):
  if self.left==None:
   self.left=value
  elif self.richt==None:
   self.richt=value
  else:
    assert False
    assert False
 def print(self):
  print(f'{self.left}{self.value}{self.richt}')
@struct
class ASSIGN:
 dst:any
 src:any
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'{self.dst}={self.src}')
@struct
class STRING:
 prefix:str
 value:str
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'{self.prefix}\'{self.value}\'')
@struct
class DECLARE:
 name:str
 type:str
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print():
  print(f'{self.name}:{self.type}')
@struct
class ENUM:
 name:str
 variants:dict[str:str|int]
 methods:list[FN]
 size:int
 def __repr__(self)->str:
  return f'{type(self).__name__}'
 def print(self):
  print(f'enum {self.name}:{self.variants}\n{self.methods}')

