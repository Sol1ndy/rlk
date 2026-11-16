execute unless entity @e[tag=rlk_body,distance=..10,limit=1] run return run function rlk:mboss/fieldgen/ai/glide_in
execute if entity @e[tag=rlk_body,distance=..6,limit=1] run return run function rlk:mboss/fieldgen/ai/glide_out
execute unless score #fgMv mb matches 0 run function rlk:mboss/fieldgen/ai/mv0
