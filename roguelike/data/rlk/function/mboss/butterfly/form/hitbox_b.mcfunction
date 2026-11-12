# Butterfly-form (the rig hovers 1.2 b, the body stays on the floor) hitbox: click shield 2.2 x 4.4 b (also for a re-created shield: cur.hit), husk scale 1.8.
data modify storage rlk:mboss cur.hit set value {w:2.2f,h:4.4f}
execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] msid run data merge entity @s {width:2.2f,height:4.4f}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run attribute @s minecraft:scale base set 1.8
