# Field (the core hangs exposed under the ring, the stack spread) hitbox: click shield 2.8 x 5.2 b (also for a re-created shield: cur.hit), husk scale 2.6.
data modify storage rlk:mboss cur.hit set value {w:2.8f,h:5.2f}
execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] msid run data merge entity @s {width:2.8f,height:5.2f}
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run attribute @s minecraft:scale base set 2.6
