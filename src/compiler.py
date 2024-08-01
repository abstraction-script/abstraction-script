from tools import *
from math import ceil
registers=['rax','rbx','rcx','rdx','r8','r9','r10','r11','r12','r13','r14','r15']

vars={}
data='\n'
bss='\n'
code='\n'
fns='\n'
optTranslate={'+':'__plus','-':'__minus','==':'__eq'}
fialdOptTranslate=0
stringLiteral=0
nestetScop=1
ifs=0

def strcompile(input:str)->str:
 out=""
 index=0
 while index<len(input)-1:
  char=input[index]
  if char=='\\':
   if input[index+1]=='n':
    out+='10,'
   else:
    raise NotImplementedError(char)
   index+=2
  else:
   out+=f"'{char}',"
   index+=1
 return out[:-1]
def error(tjeck:bool,msg:str,loc:Locale):
 if tjeck:
  print(f'compiler error at {loc.formate()},',msg)
  if DEBUG:
   assert f'compiler error at {loc.formate()}, {msg}'
  else:
   quit(1)
def warning(tjeck:bool,msg:str,loc:Locale):
 if tjeck:
  print(f'compiler warning at {loc.formate()},',msg)


from enum import Enum,auto
class Mode(enum):
  none=auto()
  src=auto()
  dst=auto()

def compilExpresion(value:token,mode:Mode)->str:
 global stringLiteral, data
 if type(value.lexeme)==FNCALL:
  code=''
  for register,arg in enumerate(value.lexeme.args):
    try:tmp=arg.lexeme.type in (tokentype.word,tokentype.numder)
    except AttributeError:
     tmp=False
    if tmp:
     if arg.lexeme.type==tokentype.word:
      try:tmp=vars[vars[arg.lexeme.lexeme]]==ENUM
      except KeyError:
        tmp=False
      if tmp: 
        error(vars[arg.lexeme.lexeme]!=vars[value.lexeme.function].signature[0][register],f'expected at agument {register} te be of type \'{vars[value.lexeme.function].signature[0][register]}\' but got \'{vars[arg.lexeme.lexeme]}\'',value.locale)
    assert arg.type==tokentype.expression
    if type(arg.lexeme)==FNCALL:
     try:vars[arg.lexeme.function]
     except KeyError:
      error(True,f'undefind function \'{arg.lexeme.function}\'',arg.locale)
     assert len(vars[arg.lexeme.function].signature.endSignature)==1 
     for reg in range(register):
      code+=f'push {registers[reg]}; all push\n'
     code+=compilExpresion(arg,mode.src)
     code+=f'mov {registers[register]},rax; retsult mov\n'
     for reg in range(register,0,-1):
      code+=f'pop {registers[reg]}; all pop\n'
    else:
     if registers[register]=='rax':
      code+=f'{compilExpresion(arg,Mode.src)}\n'
     else:
      code+=f'push rax\n{compilExpresion(arg,Mode.src)}\nmov {registers[register]},rax\npop rax\n'
  try:vars[value.lexeme.function]
  except KeyError:
   error(True,f'undefind function \'{value.lexeme.function}\'',value.locale)
  error(len(vars[value.lexeme.function].signature.beginSignature)!=len(value.lexeme.args),f'fuction \'{value.lexeme.function}\' expectd {len(vars[value.lexeme.function].signature.beginSignature)} agugent but got {len(value.lexeme.args)}',value.locale)
  error(mode==Mode.src and len(vars[value.lexeme.function].signature.endSignature)==0,f'function \'{value.lexeme.function}\' dous\'nt return anything',value.locale)
  error(mode==Mode.dst and False,f'function \'{value.lexeme.function}\' dous\'nt return a pionter',value.locale)
  warning(mode==Mode.none and len(vars[value.lexeme.function].signature.endSignature)>0,f'function \'{value.lexeme.function}\' return valu ignored',value.locale)
  if vars[value.lexeme.function].type==funcType.function:
   return f'{code}call {value.lexeme.function}\n'
  elif vars[value.lexeme.function].type==funcType.operator:
   assert len(vars[value.lexeme.function].signature.beginSignature) in (1,2)
   return f'{code}call {optTranslate[value.lexeme.function]}\n'
  else:
   assert False
 if type(value.lexeme)==DOTACSESING:
  assert value.lexeme.name.lexeme.type==tokentype.word
  var=vars[value.lexeme.name.lexeme.lexeme]
  if type(var)==ENUM:
   return compilExpresion(var.variants[value.lexeme.method.lexeme.lexeme],mode)
  if type(var)==str:
   code=''
   typ=vars[var].localsVars[value.lexeme.method.lexeme.lexeme][0].type
   if typ.isdecimal():
    size=int(typ)
   else:
    size=vars[typ].size
   ofset=vars[var].localsVars[value.lexeme.method.lexeme.lexeme][1]
   byteOfset,bitOfset=divmod(ofset,8)
   if mode==Mode.src:
    code+=f'mov rax,[q+{byteOfset}]\n'
   elif mode==Mode.dst:
    code+=f'mov rax,q+{byteOfset}\n'
   else:
    warning(True,'nothing happens here',value.locale)
   code+=f'and rax, 0b{'0'*bitOfset+'1'*size}\n'
   return code
  assert False
 if value.type==tokentype.numder:
  error(mode==Mode.dst,'numder can\'t be usde as destination',value.locale)
  warning(mode==Mode.none,'nothing happens here',value.locale)
  return f'mov rax, {value.lexeme}\n'
 if value.type==tokentype.word:
  if mode==Mode.src:
    return f'mov rax, [{value.lexeme}]\n'
  elif mode==Mode.dst:
   return f'mov rax, {value.lexeme}\n'
  else:
   warning(True,'nothing happens here',value.locale)
   return '\n'
 if value.type==tokentype.string:
  if value.lexeme.prefix=='':
   stringLiteral+=1
   data+=f"string_literal_{stringLiteral}:db {strcompile(value.lexeme.value)}\n"
   warning(mode==Mode.none,'nothing happens here',value.locale)
   return f'mov rax ,string_literal_{stringLiteral}\n'
  elif value.lexeme.prefix=='asm':
   return value.lexeme.value
  else:
   raise NotImplementedError(value)
 if value.type==tokentype.expression:
  return compilExpresion(value.lexeme,mode) 
 raise NotImplementedError(value)

def compiler(input:list[token],varPrefix='')->str:
 global nestetScop,data,fns,bss,ifs,fialdOptTranslate
 code=''
 class pythonIsStupit:
  TYPE=TYPE
  FN=FN 
  DECLARE=DECLARE
  ASSIGN=ASSIGN
  IF=IF
  ENUM=ENUM
 for index,value in enumerate(input):
  match value.type:
   case tokentype.statment:
    match type(value.lexeme):
     case pythonIsStupit.TYPE:
      vars[value.lexeme.name]=value.lexeme
     case pythonIsStupit.FN:
      vars[value.lexeme.name]=value.lexeme
      if value.lexeme.type==funcType.function:
       fns+=f'{varPrefix}{value.lexeme.name}:\n'
      elif value.lexeme.type==funcType.operator:
       try:fns+=f'{varPrefix}{optTranslate[value.lexeme.name]}:\n'
       except KeyError:
        fialdOptTranslate+=1
        optTranslate[value.lexeme.name]=f'__opt{fialdOptTranslate}'
        fns+=f'{varPrefix}{optTranslate[value.lexeme.name]}:\n'
      fns+=f"""{compiler(value.lexeme.body,varPrefix=f'__scop{nestetScop}')[0]}\n"""
      nestetScop+=1
     case pythonIsStupit.DECLARE:
      if value.lexeme.type.isdigit():
       bss+=f'{value.lexeme.name}: resb {ceil(int(value.lexeme.type)/8)}\n' 
      else:
        bss+=f'{value.lexeme.name}: resb {ceil(vars[value.lexeme.type].size/8)}\n'
      vars[value.lexeme.name]=value.lexeme.type
     case pythonIsStupit.ASSIGN:
      assert type(value.lexeme.dst.lexeme)==DOTACSESING or value.lexeme.dst.lexeme.type==tokentype.word
      code+='push rbx\n'
      code+='push rax\n'
      code+=compilExpresion(value.lexeme.dst,Mode.dst)
      code+='push rax\n'
      assert type(value.lexeme.src.lexeme)==DOTACSESING or type(value.lexeme.src.lexeme)==FNCALL or value.lexeme.src.lexeme.type==tokentype.word or value.lexeme.src.lexeme.type==tokentype.numder
      code+=compilExpresion(value.lexeme.src,Mode.src)
      code+='pop rbx\n'
      code+=f'mov [rbx], rax\n'
      code+='pop rax\n'
      code+='pop rbx\n'
     case pythonIsStupit.IF:
      ifs+=1
      elifs=0
      oldif=ifs
      code+=compilExpresion(value.lexeme.statment[0],Mode.src)#compiler(value.lexeme.statment)[0]
      code+=f'cmp rax,0\nje __elif{oldif}_1\n'
      code+=compiler(value.lexeme.block)[0]
      code+=f'jmp __endif{oldif}\n'
      for val in zip(value.lexeme.elifStatment,value.lexeme.elifBlock):
       elifStatment,elifBlock=val
       elifs+=1
       code+=f'__elif{oldif}_{elifs}:\n'
       code+=compilExpresion(elifStatment[0],Mode.src)#compiler(elifStatment)[0]
       code+=f'''cmp rax,0\nje __elif{oldif}_{elifs+1}\n'''
       code+=compiler(elifBlock)[0]
       code+=f'jmp __endif{oldif}\n'
      code+=f'__elif{oldif}_{elifs+1}:\n' 
      code+=compiler(value.lexeme.elseBlock)[0]
      code+=f'__endif{oldif}:\n'
     case pythonIsStupit.ENUM:
      vars[value.lexeme.name]=value.lexeme
     case _:
      raise NotImplementedError(value.lexeme) 
   case tokentype.expression: 
    code+=compilExpresion(value,Mode.none)+'\n'
   case tokentype.linend|tokentype.EOF:
    pass
   case _:
    raise NotImplementedError(value.lexeme)
 return code,data,bss,fns

