; generated by Aurora Compiler by Preston Hager
; https://github.com/PrestonHager/AuroraCompiler
[BITS 32]


; print a simple message.
; Arguments: [<ASTValue STRING: `Somewhere over the rainbow!`, <ASTValue STRING: `Hi`]
mov [_aurora_arg_buffer], _aurora_string_0
mov [_aurora_arg_buffer], _aurora_string_1
call print
jmp $
hlt
%include "_aurora_io"

_aurora_string0 db "Somewhere over the rainbow!"
_aurora_string1 db "Hi"