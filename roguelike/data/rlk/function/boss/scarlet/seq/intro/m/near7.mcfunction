# The skip: her on her line to the player at <= 7 b (a mv/ok point; already nearer: she stays) (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute if score #mbDist mb matches ..70 run return 0
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^3.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
