# intro: the timeline at #sq 758 (@s = the body).
execute as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"월하독작이 아니라, 대",color:"#F2D0E8"},background:-1207959552}
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
function rlk:boss/scarlet/fx/snd/scab_raise
