# event: the timeline at #sq 10 (@s = the body).
execute if score #hrEv hr matches 1 as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"조심하게. 칼자루",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 1 if entity @a[tag=player,tag=rlk_mb_camh] run as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #hrEv hr matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"한잔할 텐가? 안주",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 2 if entity @a[tag=player,tag=rlk_mb_camh] run as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
