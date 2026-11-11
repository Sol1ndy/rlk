# intro: the timeline at #sq 552 (@s = the body).
data modify storage rlk:mboss camtx.line set value {text:{text:"달과 나와 그림자 셋이 되었네..",color:"#F2D0E8"},background:-1207959552}
function rlk:mboss/cam/text
execute if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
