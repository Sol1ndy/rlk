# Human-form hitbox: click shield 1.6 x 3 b (also for a re-created shield: cur.hit), husk scale 1.4.
data modify storage rlk:mboss cur.hit set value {w:1.6f,h:3f}
execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] msid run data merge entity @s {width:1.6f,height:3f}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run attribute @s minecraft:scale base set 1.4
