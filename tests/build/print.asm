; generated by Aurora Compiler by Preston Hager
; https://github.com/PrestonHager/AuroraCompiler

mov si, _VAR_0
push si
mov si, _VAR_1
push si
mov bx, 2
call _aurora_print
jmp _aurora_end
%include "lib/_aurora_io.asm"
_VAR_0 db "Somewhere over the rainbow!", 0
_VAR_1 db "Hi", 0
_aurora_end: