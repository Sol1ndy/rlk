execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run return run function rlk:mboss/butterfly/ai/glide_in
execute if entity @e[tag=rlk_body,distance=..3.5,limit=1] run return run function rlk:mboss/butterfly/ai/glide_out
execute unless score #bfMv mb matches 0 run function rlk:mboss/butterfly/ai/mv0
