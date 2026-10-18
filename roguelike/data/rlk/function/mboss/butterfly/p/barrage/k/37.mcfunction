# barrage clock 37
function rlk:mboss/butterfly/rig/face/track
function rlk:mboss/butterfly/p/barrage/spawn4
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.2}
