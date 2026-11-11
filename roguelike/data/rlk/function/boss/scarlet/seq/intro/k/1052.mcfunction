# intro: the timeline at #sq 1052 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:{text:"신세진 것도 있겠다, 이",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute positioned 884.0 201 5.0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
function rlk:boss/scarlet/seq/intro/m/walk
function rlk:boss/scarlet/fx/snd/grass_step
