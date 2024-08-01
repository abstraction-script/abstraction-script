fn exit(int errorcode){
asm'mov rdi,rax
mov rax,60
syscall' 
}
opt +(int left,int richt)int{
 asm'add rax,rbx'
 return
}
opt -(int richt)int{
 asm'
 xor rax,0xff
 add rax,1'
 return
}

##opt -(int left,int richt)int{
 asm'sub rax,rbx'
 return
}##

exit(1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+ -20) # 100

##exit(1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+ -20-10) # 90##
