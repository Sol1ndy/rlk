# coco clock 16
function rlk:mboss/butterfly/rig/face/track
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.2}
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
