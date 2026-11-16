# ending: the timeline at #sq 1086 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:{text:"어디 보자,",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
function rlk:boss/scarlet/seq/ending/m/turn_back
