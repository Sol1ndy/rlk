# Airborne drift (@s = body, at the leap apex): 0.35 b / t toward the player (horizontal) while farther than
# 1.5 b; the floor spot below the new point must pass mv/ok.
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_body,limit=1,distance=..1.5] run return 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.35 positioned ~ 201 ~ if function rlk:mboss/mv/ok at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.35 run tp @s ~ ~ ~
