ascii:
  push ebx

  mov ebx, [_aurora_arg_buffer+4]
  mov al, [ebx]

  .done:
  pop ebx
  ret
