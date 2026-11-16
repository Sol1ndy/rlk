# intro: the timeline at #sq 914 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:{text:"곧 또 보게 될 것 같다고.",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
