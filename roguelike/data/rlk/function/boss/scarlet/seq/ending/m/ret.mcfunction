# E9 back in to 1.2 b (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^1.2 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:4}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^1.8 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:4}
