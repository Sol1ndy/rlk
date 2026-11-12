# cs1: the timeline at #sq 584 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:{text:"천지만물을 벤다는",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
