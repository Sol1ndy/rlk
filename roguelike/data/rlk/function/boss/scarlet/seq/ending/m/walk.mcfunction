# S5 the walk-in to 4.5 b (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute if score #mbDist mb matches ..50 run return 0
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^4.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:24}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^5.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:24}
