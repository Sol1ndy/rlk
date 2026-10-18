# coco clock 36
function rlk:mboss/butterfly/rig_stub/face/track
execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.12}
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.4 1 0.13
