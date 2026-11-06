# E8 the dash past the player (8 b) (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 positioned ^-1 ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:6}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 positioned ^-1 ^ ^5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:6}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 positioned ^-1 ^ ^3.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:6}
