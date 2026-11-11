# intro: the timeline at #sq 344 (@s = the body).
execute as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"벗 없이 혼자 술",color:"#F2D0E8"},background:-1207959552}
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
