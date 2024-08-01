from tools import *

words='qwertyuiopasdfghjklzxcvbnm'
words+=words.upper()
numder='0123456789'
syntaxe='{}[]()\'.,:"    \t'
opators='!@#$%^&*_+-=|\\<>'

linend=('\n',';')
keyword=('if','fn','type','opt','return','true','false','enum')
blocks={'(':')','[':']','{':'}'}
commentsConfig=[('#','\n'),('//','\n'),('##','##')]
commentsConfig.sort(key=lambda value:len(value[0]),reverse=True)
DEBUG=False

def getnessed(begin:str,end:str,input:list[token])->int:
 nessed=0
 entered=False
 for index,value in enumerate(input):
  if value.lexeme==begin:
    nessed=nessed+1
    entered=True
  elif value.lexeme==end:
    nessed=nessed-1
  if nessed==0 and entered==True:
   return index
 return None
def error(tjeck:bool,message:str,locale:Locale):
 if tjeck:
  print(f'lexer error at {locale.formate()},',message)
  if DEBUG:
   assert False,'ERROR'
  else:
   quit(1)

def tokenizing(input:str)->list[token]:
 line=1
 char=0
 tokens:list[token]=[]
 for index,value in enumerate(input):
  if value=='\n':
   line+=1
   char=0
  char+=1
  if value in words:
   typ=tokentype.word
  elif value in numder:
   typ=tokentype.numder
  elif value in syntaxe:
   typ=tokentype.syntax
  elif value in opators:
   typ=tokentype.opator
  elif value in linend:
    typ=tokentype.linend
  else:
   error(True,f'unknow symbol \'{value}\'',Locale(line,char))
  tokens.append(token(typ,value,Locale(line,char)))
 return tokens
def strings(input:list[token])->list[token]:
 tokens:list[token]=[]
 index=0
 while index<len(input):
  value=input[index]
  if value.lexeme in ("'",'"'):
   for ind,val in enumerate(input[index+1:]):
    if (val.lexeme==value.lexeme) and (input[index+1:][ind-1].lexeme!='\\'):
     break
   tokens.append(token(tokentype.string,tokensToString(input[index+1:ind+index+1]),value.locale))
   index+=ind+1
  else:
   tokens.append(value) 
  index+=1
 return tokens
def comments(input:list[token])->list[token]:
 index=0
 tokens:list[token]=[]
 while index<len(input):
  value=input[index]
  add=True
  for ind,val in enumerate(commentsConfig):
   if tokensToString(input[index:index+len(val[0])])==val[0]:
    add=False
    index+=len(val[0])
    for i,v in enumerate(input[index:]):
     if tokensToString(input[index+i:index+i+len(val[1])])==val[1]:
      index+=len(val[1])+i-1
      tokens.append(token(tokentype.linend,'\n',None))
      break
    break
   if add==False:break
  if add==True:
   tokens.append(value)
  index+=1
 return tokens
def merging(input:list[token])->list[token]:
 tokens:list[token]=[token(tokentype.BOF,'',Locale(None,None))]
 for index,value in enumerate(input):
  if (tokens[-1].type==value.type and value.type!=tokentype.syntax) or (tokens[-1].type==tokentype.word and value.type==tokentype.numder)or(tokens[-1].type in (tokentype.word,tokentype.numder) and value.lexeme=='_'):
   tokens[-1].lexeme+=value.lexeme
  elif tokens[-1].type==tokentype.word and value.type==tokentype.string:
   prefix=tokens[-1].lexeme
   string=value.lexeme
   tokens[-1]=token(tokentype.string,STRING(prefix,string),tokens[-1].locale)
  elif value.type==tokentype.string:
   prefix=''
   string=value.lexeme
   tokens.append(token(tokentype.string,STRING(prefix,string),value.locale))
  else:
   tokens.append(value)
 return tokens
def cleaning(input:list[token])->list[token]: 
 tokens:list[token]=[]
 for index,value in enumerate(input):
  if value.lexeme==' ':
   pass
  elif value.lexeme=='=':
   tokens.append(token(tokentype.syntax,'=',value.locale))
  elif value.lexeme in keyword:
   tokens.append(token(tokentype.keyword,value.lexeme,value.locale))
  else: 
   tokens.append(value)
 return tokens
def block(input:list[token])->list[token]:
 tokens:list[token]=[]
 index=0
 while index<len(input):
  value=input[index]
  try:tmp=value.lexeme in blocks.keys()
  except TypeError:
   tmp=False
  if tmp:
   begin=value.lexeme
   end=blocks[begin]
   tmp=getnessed(begin,end,input[index:])
   error(tmp==None,f'{value.lexeme} was never closed',value.locale)
   ind=tmp+index
   begin=input[index]
   end=input[ind]
   inp=block(input[index+1:ind])
   tokens.append(begin)
   tokens.append(token(tokentype.block,inp,value.locale))
   tokens.append(end)
   index=ind
  else:
   tokens.append(value)
  index+=1
 return tokens

def lexer(input:str)->list[token]:
 tokens=tokenizing(input)
 tokens=strings(input=tokens)
 tokens=comments(input=tokens)
 tokens=merging(input=tokens)
 tokens=cleaning(input=tokens)
 tokens=block(input=tokens)
 tokens.append(token(tokentype.EOF,'',Locale(None,None)))
 return tokens

