fn exit(int errorcode){
asm'mov rdi,rax
mov rax,60
syscall' 
}
opt +(int x,int y)int{
 asm'add rax, rbx'
 return
}
opt ==(int x,int y)bool{
 asm'cmp rax, rbx
 je .true
 .false:
 mov rax, 0
 ret
 .true:
 mov rax, 1'
 return 
}

type int{
    64 self
}

int q=99
if q+3==4{
    exit(1)
    exit(2)}
elif q==3{
    exit(8)}
else{
    exit(3)}
exit(4)
