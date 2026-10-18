# coco clock 14
function rlk:mboss/butterfly/rig_stub/face/track
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.2}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
