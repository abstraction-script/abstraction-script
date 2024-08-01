type int{
 64 self
}

type str{
 64 self # pointer
}


fn write(int fd,str mgs,int len){
asm'mov rdi,rax
mov rsi,rbx
mov rdx,rcx
mov rax,1
syscall'
return
}

write(1,'Hello, World!\n',14)

fn exit(int errorcode){
asm'mov rdi,rax
mov rax,60
syscall' 
}

exit(0)
