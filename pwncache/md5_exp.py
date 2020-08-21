from pwn import *
from pwnlib.util.packing import p32
# context(log_level="debug")

p = remote('pwnable.kr', 9002)
p.recvuntil("input captcha : ")
captcha = p.recvline()
p.sendline(captcha)
print(captcha)


p.recvuntil("Encode your data with BASE64 then paste me!\n")
p.sendline('aaaaaaa')

# base = int.from_bytes(putchar, "little") - libc.symbols['putchar']

p.interactive()
p.close()

# pwn
# Base64Decode -> var_20ch
# cal_md5 <- var_20ch
    # -> eax -> var_210h

# could be var_20c overwriting stack addr in decode or cal_md5
# could it be captcha related? like srand?
