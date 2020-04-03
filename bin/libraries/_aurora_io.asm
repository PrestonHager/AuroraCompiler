; _aurora_io.asm
; by Preston Hager
; for Aurora Compiler

io_out:
  push eax

  .done:
  pop eax
  ret

print:
  push eax
  push ebx
  
  mov si, [_aurora_arg_buffer+4]
  mov ebx, 0x8b000
  
  .repeat:
    mov al, byte [si]
    inc si
    cmp al, 0
    je .done
    mov [ebx], al
    add ebx, 2
    jmp .repeat
  
  .done:
  pop eax
  pop ebx
  ret
  
println:
  call print
  mov [_aurora_arg_buffer+4], word NEWLINE
  call print
  ret
  
NEWLINE db 0x10, 0