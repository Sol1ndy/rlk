# Spot back (@s = the body): R2: the retreat 6 b straight away from the player (shorter / sideways when blocked; else she stays). The first candidate passing mv/ok (MOVE_R 22.5, feet and head
# free) gets the marker rlk_hr_gsp; else her own spot, walked toward the axis until mv/ok passes.
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^6 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^4.5 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^3 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~270 0 positioned ^ ^ ^4 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~90 0 positioned ^ ^ ^4 if function rlk:mboss/mv/ok run return run function rlk:boss/scarlet/g/spot/put
execute at @s positioned ~ 201 ~ run function rlk:boss/scarlet/g/spot/put
scoreboard players set #g_c hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s run function rlk:boss/scarlet/g/spot/clamp
