# Groggy (slumped) hitbox: click shield 2.6 x 3.6 b (also for a re-created shield: cur.hit), husk scale 2.
data modify storage rlk:mboss cur.hit set value {w:2.6f,h:3.6f}
execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] msid run data merge entity @s {width:2.6f,height:3.6f}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run attribute @s minecraft:scale base set 2
