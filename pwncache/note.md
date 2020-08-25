# EXP note

* Stack might not work all time. Unintentional overwrite could happen.
A good rule is to use heap or any memory address if double reference could happen.

* GOT table could be randomized if PIC is enabled. The shared libc is loaded lazily so the original jmp target is probably a sym..got functions. (View imports with ia in r2)

* Canary is stored before old ebp and is usually copied from fs or gs segment register.
If the check failed, stack_chk_failed would be called. (GOT hijack)

