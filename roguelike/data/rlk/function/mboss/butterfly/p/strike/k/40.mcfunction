# strike clock 40
function rlk:mboss/butterfly/rig/face/track
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.06}
playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
