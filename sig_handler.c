#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <ucontext.h>

static void sighandler(int signo, siginfo_t *si, void* v_context)
{
    ucontext_t *context = v_context;
    context->uc_mcontext.gregs[REG_RIP] += 10;
}

int *totally_null_pointer = NULL;

int main() {
    struct sigaction psa;
    psa.sa_sigaction = sighandler;
    sigaction(SIGSEGV, &psa, NULL);

    printf("Before NULL pointer dereference\n");
    *totally_null_pointer = 1;
    __asm__ __volatile__("nop;nop;nop;nop;nop;nop;nop;nop;nop;nop;");
    printf("After NULL pointer. Still here!\n");

    return 0;
}
