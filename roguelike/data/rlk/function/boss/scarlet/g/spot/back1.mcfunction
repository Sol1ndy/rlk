# Spot back1 (@s = the body): R2: the step back 1 b (else she stays). The first candidate passing mv/ok (MOVE_R 22.5, feet and head
# free) gets the marker rlk_hr_gsp; else her own spot, walked toward the axis until mv/ok passes.
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^1 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ run function rlk:boss/scarlet/g/spot/put
scoreboard players set #g_c hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s run function rlk:boss/scarlet/g/spot/clamp
