# intro: the timeline at #sq 690 (@s = the body).
execute unless entity @a[tag=player,tag=rlk_mb_camh] run function rlk:boss/scarlet/fx/hud/line {id:5}
execute as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"그리",color:"#F2D0E8"},background:-1207959552}
execute if entity @a[tag=player,tag=rlk_mb_camh] run as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
