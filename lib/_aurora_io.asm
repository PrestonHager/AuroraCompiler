_aurora_print:
  pusha
  pop si
  mov ah, 0Eh     ; Function code

.repeat:
  lodsb				    ; Get char from string
  cmp al, 0
  je .done_str    ; If char is zero, finish
  int 10h				  ; Else, call 10h interrupt
  jmp .repeat			; And then loop

.done_str:
  dec bx
  cmp bx, 0
  je .done
  pop si
  jmp .repeat

.done:          ; finish function
  popa
  ret
