from sys import argv as args
from os import system as shell

from lexer import lexer
from parser import parser
from compiler import compiler

if len(args)!=2:
 print(f'usage: {args[1]} <file>')

input=open(args[1]).read()

input=lexer(input)
#print('lexer out',input)

input=parser(input)
input=input[2]+input[1]+input[0]
#print('parser out:',input)

code,data,bss,fns=compiler(input)

out=f"""global _start
segment .data
{data}
segment .bss
{bss}
segment .text
{fns}
_start:
{code}"""
open('out.asm','w').write(out)
shell('nasm -f elf64 -o out.o out.asm')
shell('ld out.o -o out.elf')
shell('rm out.o')
shell('strip out.elf')

'''
plan:
clean up,spel chek,beter error msg
bediging
new git repo on new acount
scop fix via pars
function overloot
recursion
jmp label
loops
type tjeking
gen yield
for loop
arry indexing
import
inetsion
stdlib
brain f*ck compiler program
'''