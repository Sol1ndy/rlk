# sweep clock 50
function rlk:mboss/butterfly/rig_stub/face/track
execute if entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.25}
playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.4 1.5 0.13
