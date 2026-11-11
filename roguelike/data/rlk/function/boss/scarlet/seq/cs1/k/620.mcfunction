# cs1: the timeline at #sq 620 (@s = the body).
execute as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"이런 것일",color:"#F2D0E8"},background:-1207959552}
execute if entity @a[tag=player,tag=rlk_mb_camh] run as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.1 ^1 ^0.62 run function rlk:boss/scarlet/fx/p/glint {c:5}
