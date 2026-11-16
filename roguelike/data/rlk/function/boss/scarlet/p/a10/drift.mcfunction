# A10 apex drift (@s = the body, ticks 9-13): 0.4 b toward the player while farther than 1.5 b
# (horizontal; the floor point below must pass mv/ok).
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_body,limit=1,distance=..3.0] run return 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.4 positioned ~ 201 ~ if function rlk:mboss/mv/ok at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.4 run tp @s ~ ~ ~
