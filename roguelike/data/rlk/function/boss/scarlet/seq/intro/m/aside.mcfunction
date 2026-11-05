# Beside the seat stone: 1.1 b to her right (else her left) over 20 t, before the turn (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @s rotated as @s rotated ~ 0 positioned ^-1.1 ^ ^ positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:20}
execute at @s rotated as @s rotated ~ 0 positioned ^1.1 ^ ^ positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:20}
