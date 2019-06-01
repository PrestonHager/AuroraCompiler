; _aurora_string.asm
; by Preston Hager
; for Aurora Compiler

; get the "string" that is passed in, and load the first character into al.
ascii:
  push ebx

  mov ebx, [_aurora_arg_buffer+4]
  mov al, [ebx]

  .done:
  pop ebx
  ret

; loop over the string that's passed in, until a null (0) character.
len:
  push ebx
  mov eax, [_aurora_arg_buffer+4]

  .repeat:
    mov bl, [eax]     ; load the next character
    cmp bl, 0         ; if it's null, jump to .done
    je .done
    inc eax           ; otherwise increase index and counter and repeat
    jmp .repeat

  .done:
  ; calculate the actual length by subtracting the pointer from the current index.
  mov ebx, [_aurora_arg_buffer+4]
  sub eax, ebx
  pop ebx
  ret
