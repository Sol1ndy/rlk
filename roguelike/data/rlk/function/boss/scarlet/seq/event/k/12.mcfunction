# event: the timeline at #sq 12 (@s = the body).
execute if score #hrEv hr matches 1 as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"조심하게. 칼자루를 쥐",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 1 if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #hrEv hr matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"한잔할 텐가? 안주는 달",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 2 if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/anchor/hand_r
execute if score #hrEv hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/ev_glint
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_chime
