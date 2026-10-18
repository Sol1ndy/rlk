scoreboard players add #bfT mb 1
function rlk:mboss/butterfly/rig_stub/face/track
# Pyro patterns want 6-8 b
execute if score #bfWant mb matches 1 if entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/mv/away {d:0.25}
execute if score #bfT mb matches 8.. run function rlk:mboss/butterfly/ai/go
