type uint64{
   64 self 
}

fn exit(int errorcode){ # uint8
asm'mov rdi,rax
mov rax,60
syscall' 
}

opt +(int x,int y)int{
 asm'add rax,rbx'
 return
}

uint64 q
uint64 w=9
q=2+6
exit(q+w) # 17

