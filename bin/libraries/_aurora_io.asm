_aurora_print:
  pusha
  mov eax, 0xb8000
  mov [eax], byte 'A'
  call _aurora_get_cursor

.repeat:
  ; move the pointer at [_AURORA_STRING_ARG_BUFFER+ax] into esi, and print
  mov edx, _AURORA_STRING_ARG_BUFFER
  mov si, [edx]
.print:
  lodsb
  cmp al, 0
  je .done_str
  mov [eax], al
  jmp .print

.done_str:
  add edx, 4    ; increase index by 4
  dec bx        ; decrease total argument by 1
  cmp bx, 0     ; if no more argument, .done
  je .done
  jmp .repeat

.done:          ; finish function
  popa
  ret

_aurora_get_cursor:
  push bx
  push dx
  mov bx, 0           ; return with the cursor position of video memeory in eax but for now store in bx

  .low_byte:          ; the low byte is al
  mov al, 0x0f        ; ask for low byte
  mov dx, 0x03D4      ; index vga port
  out dx, al          ; out io
  mov dx, 0x03D5      ; data vga port
  in al, dx           ; in io
  mov bl, al          ; move value into low byte of bx

  .high_byte:         ; the high byte is ah
  mov al, 0x0e        ; ask for high byte
  mov dx, 0x03D4      ; index vga port
  out dx, al
  mov dx, 0x03D5      ; data vga port
  in al, dx
  mov bh, al          ; move value into high byte of bx

  .done:
  mov ax, bx        ; put ebx into eax.
  pop dx
  pop bx
  ret                 ; pop and return
