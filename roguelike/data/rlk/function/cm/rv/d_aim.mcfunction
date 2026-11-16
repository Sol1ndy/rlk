# 14 t: the landing point follows the body's feet (dropped onto the ground), then locks for the last 6 t
scoreboard players operation @s cmT -= #eStep tmp
execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_rv_tsel
execute unless entity @e[tag=rlk_rv_tsel,limit=1] run return run function rlk:cm/rv/d_abort
execute unless entity @s[tag=rlk_rv_lk] as @e[tag=rlk_rv_tsel,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:cm/rv/d_track
execute if score @s cmT matches ..6 unless entity @s[tag=rlk_rv_lk] unless function rlk:cm/rv/d_lock run return run function rlk:cm/rv/d_abort
scoreboard players set #lk tmp 0
execute if entity @s[tag=rlk_rv_lk] run scoreboard players set #lk tmp 1
scoreboard players set #n tmp 32
execute at @e[tag=rlk_rv_tsel,limit=1] facing entity @s feet rotated ~ 0 run function rlk:cm/rv/line
execute if entity @s[tag=rlk_rv_lk] at @e[tag=rlk_rv_tsel,limit=1] run particle minecraft:flame ~ ~0.1 ~ 0.25 0 0.25 0.01 2
execute if score @s cmT matches ..0 run function rlk:cm/rv/d_go
tag @e[tag=rlk_rv_tsel] remove rlk_rv_tsel
