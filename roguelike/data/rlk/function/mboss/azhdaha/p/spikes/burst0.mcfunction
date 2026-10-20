# At point 1 (t76): the planted spike bursts (crystal-blade crown in the ground element).
execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/crown/1
execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/crown/2
execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/crown/3
execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/crown/4
execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/crown/5
function rlk:mboss/azhdaha/fx/snd/spikes_explode
particle minecraft:block{block_state:"minecraft:raw_gold_block"} ~ ~1 ~ 0.6 0.8 0.6 0.1 18 force @a[tag=player]
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p4s0]
