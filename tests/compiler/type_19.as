

type t{
 64 v
}

fn exit(int errorcode){
asm'mov rdi,rax
mov rax,60
syscall' 
}

t q
q.v=19
exit(q.v)

