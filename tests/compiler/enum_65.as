fn exit(int errorcode){
asm'mov rdi,rax
mov rax,60
syscall' 
}

enum ascii{
  A=64
  B=65
}
ascii q=ascii.B
exit(q) # can be itupte as int or ascii but int cant be itupte as ascii
