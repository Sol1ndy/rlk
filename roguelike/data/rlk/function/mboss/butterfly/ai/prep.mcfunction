scoreboard players add #bfT mb 1
function rlk:mboss/butterfly/rig/face/track
scoreboard players set #bfPNeed mb 0
# Pyro patterns want 6-8 b: back off at 0.25 b/t (inside r 16.5)
execute if score #bfWant mb matches 1 if entity @e[tag=rlk_body,distance=..6,limit=1] run scoreboard players set #bfPNeed mb 1
execute if score #bfWant mb matches 1 if entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.25}
# 달빛 해제 starts within 8 b: glide in at 0.4 b/t, at most 10 t (its swoop stays near 1 b/t)
execute if score #bfPick mb matches 15 unless entity @e[tag=rlk_body,distance=..8,limit=1] run scoreboard players set #bfPNeed mb 1
execute if score #bfPick mb matches 15 unless entity @e[tag=rlk_body,distance=..8,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.4}
# a switched look always waits 8 t; then go once nothing is left to do, or at the cap
execute if score #bfPSw mb matches 1 if score #bfT mb matches ..7 run return 0
execute if score #bfPNeed mb matches 0 run return run function rlk:mboss/butterfly/ai/go
execute if score #bfPick mb matches 15 if score #bfT mb matches 10.. run return run function rlk:mboss/butterfly/ai/go
execute unless score #bfPick mb matches 15 if score #bfT mb matches 8.. run return run function rlk:mboss/butterfly/ai/go
