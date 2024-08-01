from tools import *

from enum import Enum as enum
from enum import auto

vars={}
precedens=(('+','-'),('*','/'),('^'))

def getPrecedence(input:str)->int:
 assert type(input)==str
 for index,value in enumerate(precedens):
  if input in value:
    return index 
 return 0
def getUntil(string:str,input:list[token],lexeme=True)->int:
 for index,value in enumerate(input):
  if (value.lexeme==string and lexeme==True) or (value.type==string and lexeme==False):
   return index
def getUntilBlock(string:str,input:list[token])->int:
 for index,value in enumerate(input):
  if value.type==tokentype.block and value.lexeme==string:
   return index
def addRitchs(dst:AST,src:AST)->AST:
 if dst.richt==None:
  dst.add(src)
  return dst
 else:
  dst.richt=addRitchs(dst.richt,src)
  return dst
def astToFncalls(ast:AST)->token:
 if type(ast)!=AST:
  return ast
 call=FNCALL(ast.value.lexeme,(astToFncalls(ast.left),astToFncalls(ast.richt)))
 return token(tokentype.expression,call,ast.value.locale)
def error(tjeck:bool,msg:str,loc:Locale):
 if tjeck:
  print(f'parser error at {loc.formate()},',msg)
  if DEBUG:
   assert False,f'parser error at {loc.formate()}, {msg}'
  else:
   quit(1)

def keywords(input:list[token])->tuple[list[token],list[token],list[token]]:
 parsed:list[token]=[]
 types:list[token]=[]
 functions:list[token]=[]
 index=0
 while index<len(input):
  value=input[index]
  if value.type!=tokentype.keyword:
   parsed.append(value)
   index+=1
   continue
  match value.lexeme:
   case 'if':
    tmp=getUntil('{',input[index:])
    error(tmp==None,'expectd if <statment> {...}',value.locale)
    ind=tmp+index
    error(input[index+1:ind]==[],'expectd a statment',value.locale)
    statment=parser(input[index+1:ind])[0]
    input[ind+1].lexeme
    block=parser(input[ind+1].lexeme)[0]
    ind+=3
    if input[ind].type==tokentype.linend:
      ind+=1
    elifStatment=[]
    elifBlock=[]
    elseBlock=[]
    while ...:
     if input[ind].lexeme=='elif':
      tmp=getUntil('{',input[ind:])
      error(tmp==None,'expectd if <statment> {...}',input[ind].locale)
      i=tmp+ind
      error(input[ind+1:i]==[],'expectd a statment',input[ind].locale)
      elifStatment.append(parser(input[ind+1:i])[0])
      elifBlock.append(parser(input[i+1].lexeme)[0])
      ind=i+3
      if input[ind].type==tokentype.linend:
       ind+=1
     elif input[ind].lexeme=='else':
      error(input[ind+1].lexeme!='{','expectd else {...}',input[ind+1].locale)
      elseBlock=parser(input[ind+2].lexeme)[0]
      ind+=4
      break
     else:
      break
    index=ind-1
    parsed.append(token(tokentype.statment,IF(statment,block,elifStatment,elifBlock,elseBlock),input[index].locale))
   case 'fn'|'opt':
    if value.lexeme=='fn':
     error(input[index+1].type!=tokentype.word,'expected a vaild variabe name',input[index+1].locale)
     typ=funcType.function
    elif value.lexeme=='opt':
     error(input[index+1].type!=tokentype.opator,'expected a vaild opator symbol',input[index+1].locale)
     typ=funcType.operator
    else: 
      assert False
    error(input[index+2].lexeme!='(','expected (',input[index+2].locale)
    name=input[index+1].lexeme
    inp=input[index+3].lexeme
    ind=0
    loacalVars={}
    beginSignature=[]
    while ind<len(inp):
     val=inp[ind]
     error(inp[ind].type!=tokentype.word and inp[ind].type!=tokentype.numder,'expected the name of a type or a size as numder',inp[ind].locale)
     error(inp[ind+1].type!=tokentype.word,'expected a vaild variabe name',inp[ind+1].locale)
     error(len(inp)-1>=ind+2 and inp[ind+2].lexeme!=',' , 'expected ,',inp[ind].locale)
     ty=val.lexeme
     argName=inp[ind+1].lexeme
     beginSignature.append(ty)
     ind+=3
     loacalVars[argName]=VAR(argName,ty)

    endSignature=input[index+5:getUntil('{',input[index+5:])+index+5]
    signature=Signature(beginSignature,endSignature)
    assert len(input[index+5+len(endSignature)+1:getUntil('}',input[index+5+len(endSignature)+1:])+index+5+len(endSignature)+1])==1
    body=parser(input[index+5+len(endSignature)+1:getUntil('}',input[index+5+len(endSignature)+1:])+index+5+len(endSignature)+1][0].lexeme)
    assert body[1]==[] # type and function defi  not impletet in fn body
    assert body[2]==[]
    body=body[0]
    nf=FN(name,typ,loacalVars,signature,body)
    if nf.name in vars.keys() and nf.signature in vars[nf.name]:
     parsed.append(token(tokentype.statment,nf,value.locale))
    else:
      functions.append(token(tokentype.statment,nf,value.locale))

    index+=8+len(endSignature)
   case 'type':
    error(input[index+1].type!=tokentype.word,f'expected a vaild variabe name',input[index+1].locale)
    name=input[index+1].lexeme
    error(input[index+2].lexeme!='{','expected {',input[index+2].locale)
    size=0
    ind=0
    inp=input[index+3].lexeme
    localsVars={}
    while ind<len(inp):
     val=inp[ind]
     if val.lexeme=='\n':
      error(inp[ind+1].type!=tokentype.word and inp[ind+1].type!=tokentype.numder,f'expected a vaild variabe name or numder',inp[ind+1].locale)
      error(inp[ind+2].type!=tokentype.word,f'expected a vaild variabe name',inp[ind+2].locale)
      try:tmp=inp[ind+3].lexeme!='\n'
      except NotImplementedError():
       tmp=False
      error(tmp,f'expected a new line',inp[ind+3].locale)
      ind+=1
      continue
     if val.type in (tokentype.word,tokentype.numder) and inp[ind+1].type==tokentype.word and inp[ind+2].lexeme=='\n':
      attributeName=inp[ind+1].lexeme
      val=None
      typ=inp[ind].lexeme
      localsVars[attributeName]=(VAR(attributeName,typ),size)
      if inp[ind].type==tokentype.word:
       try:size+=vars[inp[ind].lexeme].size
       except KeyError:
        error(True,f'undefind type \'{inp[ind].lexeme}\'',inp[ind].locale)
      elif inp[ind].type==tokentype.numder:
       size+=int(inp[ind].lexeme)
      ind+=2
     else:
      break
     ind+=1
    typ=TYPE(name,localsVars,size)
    if name in vars.keys():
     parsed.append(token(tokentype.statment,typ,value.locale))
    else:
      types.append(token(tokentype.statment,typ,value.locale))
    index+=4
   case 'enum':
    name=input[index+1].lexeme
    error(input[index+1].type!=tokentype.word,f'expected a vaild variabe name',input[index+1].locale)
    variants={}
    error(input[index+2].lexeme!='{','expected {',input[index+2].locale)
    inp=input[index+3].lexeme
    ind=0
    size=64 #tmp
    while ind<len(inp)-1:
     val=inp[ind]
     if val.type==tokentype.linend:
      error(inp[ind+1].type!=tokentype.word,'expected vaild variable',inp[ind+1].locale)
      error(inp[ind+2].lexeme!='=','expected =',inp[ind+1].locale)
      error(type(getUntil('\n',inp[ind+2:]))!=int,'expected new line after expresion',inp[ind+3].locale)
      ind+=1
      continue
     if val.type!=tokentype.word:
      break
     variants[val.lexeme]=inp[ind+2]
     ind+=3
    parsed.append(token(tokentype.statment,ENUM(name,variants,{},size),value.locale))
    index+=ind-2-1
   case 'return':
    parsed.append(token(tokentype.string,STRING('asm','ret'),value.locale))
   case 'true':
    parsed.append(token(tokentype.string,STRING('asm','mov rax,1\n'),value.locale))
   case 'false':
    parsed.append(token(tokentype.string,STRING('asm','mov rax,0\n'),value.locale))
   case _:
    assert False,f'unhandled keyword {value.lexeme}'
  index+=1
 return parsed,functions,types
def generalizing(input:list[token])->list[token]:
 out=[]
 index=0
 while index<len(input):
  value=input[index]
  if value.type in (tokentype.word,tokentype.numder,tokentype.string):
   out.append(token(tokentype.expression,value,value.locale))
  else:
   out.append(value)
  index+=1
 return out 
def expesions(input:list[token])->list[token]:
 parsed=[]
 index=0
 while index<len(input)-1:
   value=input[index]
   if value.type!=tokentype.expression:
    parsed.append(value)
    index+=1
    continue
   match input[index+1].lexeme:
    case '(':
     function=value.lexeme.lexeme
     args=[[]]
     for ind,val in enumerate(input[index+2].lexeme):
      if val.lexeme==',':
       arg=parser(args[-1])[0]
       assert len(arg)==1
       args[-1]=arg[0]
       args.append([])
      else:
       args[-1].append(val)
     args[-1]=parser(args[-1])[0]
     if len(args[-1])==1:
      args[-1]=args[-1][0]
     elif len(args[-1])==0:
       args=[]
     else:
       assert False
     args=args
     parsed.append(token(tokentype.expression,FNCALL(function,args),value.locale))
     index+=3
     return expesions(parsed+input[index+1:])
    case '.':
     name=value
     assert input[index+2].type==tokentype.expression
     method=input[index+2]
     parsed.append(token(tokentype.expression,DOTACSESING(name,method),value.locale))
     index+=2
     return expesions(parsed+input[index+1:])
    case '[':
     assert False
    case _:
     parsed.append(value)
   index+=1
 return parsed+input[index:]
def unaryOperator(input:list[token])->list[token]:
 index=0
 while index<len(input):
  value=input[index]
  if input[index-1].type!=tokentype.expression and value.type==tokentype.opator and input[index+1].type==tokentype.expression:
   function=value.lexeme
   args=[input[index+1]]
   input[index]=token(tokentype.expression,FNCALL(function,args),value.locale)
   input=input[:index+1]+input[index+2:]
   return unaryOperator(input)
  index+=1
 return input
def binaryOperator(input:list[token])->list[token]:
 out=[]
 def order(input:list[token])->AST:
  ast=AST()
  index=0
  while index<len(input):
   value=input[index]
   if type(value)==AST:
    ast.add(value)
   elif value.type==tokentype.opator:
    A=getPrecedence(value.lexeme)
    try:B=getPrecedence(input[index+2].lexeme)
    except IndexError:
     assert ast.left!=None and ast.value==None and ast.richt==None
     ast.value=value
     ast.add(input[index+1])
     return ast
    if len(input)-1<index+2:
     raise NotImplementedError
    elif A>=B:
     assert ast.left!=None and ast.richt==None
     ast.value=value
     # power is special
     if value.lexeme=='^' and input[index+2].lexeme=='^':
      newast=AST()
      i=index+2
      while i<len(input):
       if newast.left==None:
        newast.add(input[i-1])
        newast.value=input[i]
       elif input[i].lexeme!='^':
        break
       else:
        tmpast=AST()
        tmpast.add(input[i-1])
        tmpast.value=input[i]
        newast=addRitchs(newast,tmpast)      
       i+=2
      newast=addRitchs(newast,input[i-1])
      ast.add(newast)
      newast=ast
      index=i-1
     else:
      ast.add(input[index+1])
      newast=AST()
      newast.add(ast)
      newast.value=input[index+2]
      if len(input)-1<index+4:
       newast.add(input[index+3])
      elif B<getPrecedence(input[index+4].lexeme):
       i=0
       while ...:
        if len(input)-1<index+4+i or B>=getPrecedence(input[index+4+i].lexeme):
         break
        i+=2
       i-=1
       tmpast=order(input[index+3:index+4+1+i])
       newast.add(tmpast)
       index+=i+1
      elif B>=getPrecedence(input[index+4].lexeme):
       i=0
       while ...:
        if len(input)-1<index+4+i or B<getPrecedence(input[index+4+i].lexeme):
         break
        i+=2
       ii=0
       while ...:
        if len(input)-1<index+i+4+ii or getPrecedence(input[index+i+4].lexeme)<getPrecedence(input[index+4+i+ii].lexeme):
         break
        ii+=2
       if input[index+i+3:index+i+ii+1-1]==[]:
        hast=input[-1]
       else:
        hast=order(input[index+i+3:index+i+ii+1-1])
       newast=order([ast]+input[index+2:index+4+1+i+1-3]+[hast])
       index+=4+1+i+1-3
      index+=3
 
     ast=AST()
     ast.add(newast)
    elif A<B:
     ast.value=value
     newast=AST()
     newast.add(input[index+1])
     newast.value=input[index+2]
     if len(input)-1<index+4:
      newast.add(input[index+3])
      index+=2
     elif B>=getPrecedence(input[index+4].lexeme):
      i=index+2
      while i<len(input):
       if A>=getPrecedence(input[i].lexeme):
        break
       i+=2
      newast=order(input[index+1:i]) 
      index=i-1
     else: 
      i=0
      while ...:
       if B>=getPrecedence(input[index+4].lexeme) or len(input)-1<index+4+i:
        break
       i+=1
      newast.add(order(input[index+3:index+4+2+i]))
      index+=i
     ast.add(newast)
     q=AST()
     q.add(ast)
     ast=q
   else:
    ast.add(value)
   index+=1
  assert ast.value==None,ast.richt==None
  ast=ast.left
  return ast
 # 1x(2+3) -> 1xast
 index=0
 while len(input)!=index:
  value=input[index]
  if value.lexeme=='(':
   out.append(token(tokentype.expression,order(input[index+1].lexeme),value.locale))
   index+=2  
  else:
   out.append(value)
  index+=1
 input=out
 out=[]
 # 1x2+3 -> ast
 index=0
 while index<len(input):
  value=input[index]
  try:
   input[index+1]
  except IndexError:
   out.append(value)
   break 
  if value.type in  (tokentype.expression,tokentype.numder) and input[index+1].type==tokentype.opator:
   for ind,val in enumerate(input[index:]):
    if val.type not in (tokentype.expression,tokentype.opator,tokentype.numder,tokentype.word):
     break
   else:
    ind+=1
   ind-=1
   tok=astToFncalls(order(input[index:index+ind+1]))
   tok.locale=value.locale
   out.append(tok)
   index+=ind+1
  else:
   out.append(value)
   index+=1 
 return out
def assingAndDeclartions(input:list[token])->list[token]:
 out=[]
 index=0
 while index<len(input):
  value=input[index]
  try:tmp1=value.lexeme.type in (tokentype.word,tokentype.numder) and input[index+1].type==tokentype.expression and input[index+2].lexeme!='='
  except (IndexError,AttributeError):tmp1=False
  try:tmp2=value.lexeme.type in (tokentype.word,tokentype.numder) and input[index+1].type==tokentype.expression and input[index+2].lexeme=='='
  except (IndexError,AttributeError):tmp2=False
  try:tmp3=(input[index-1].type!=tokentype.expression or input[index-1].lexeme.type!=tokentype.word) and value.type==tokentype.expression and input[index+1].lexeme=='='
  except (IndexError,AttributeError):tmp3=False
  if tmp1:
   typ=value.lexeme.lexeme
   name=input[index+1].lexeme.lexeme
   out.append(token(tokentype.statment,DECLARE(name,typ),value.locale))
   index+=2
  elif tmp2:
   typ=value.lexeme.lexeme
   name=input[index+1].lexeme.lexeme
   out.append(token(tokentype.statment,DECLARE(name,typ),value.locale))
   assert value.type==tokentype.expression and input[index+3].type==tokentype.expression 
   dst=input[index+1]
   src=input[index+3]
   out.append(token(tokentype.statment,ASSIGN(dst,src),value.locale))
   index+=5
  elif tmp3:
   assert value.type==tokentype.expression and input[index+2].type==tokentype.expression 
   dst=value
   src=input[index+2]
   out.append(token(tokentype.statment,ASSIGN(dst,src),value.locale))
   index+=3
  else:
   out.append(value)
   index+=1

 #clean up of newline
 input=out
 out=[]
 index=0
 for index,value in enumerate(input):
  if value.type==tokentype.linend and index!=len(input)-1 and input[index+1].type==tokentype.linend or value.type==tokentype.BOF:
   continue
  if value.type==tokentype.linend:
   out.append(token(tokentype.linend,'\n',input[index].locale))
  else:
   out.append(value)

 return out


def parser(input:list[token])->list[token|AST]:
 parsed,functions,types=keywords(input)
 out=generalizing(parsed)
 out=expesions(input=out)
 out=unaryOperator(input=out)
 out=binaryOperator(input=out)
 out=assingAndDeclartions(input=out)
 
 return out,functions,types







