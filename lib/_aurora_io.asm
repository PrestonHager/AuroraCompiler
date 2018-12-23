_aurora_print:
  pusha
  mov ax, 0

.repeat:
  ; move the pointer at [_AURORA_STRING_ARG_BUFFER+ax] into esi, and print
  mov esi, [_AURORA_STRING_ARG_BUFFER+ax]
  call graphics_print_string

.done_str:
  inc ax        ; increase index by 1
  dec bx        ; decrease total argument by 1
  cmp bx, 0     ; if no more argument, .done
  je .done
  jmp .repeat

.done:          ; finish function
  popa
  ret
