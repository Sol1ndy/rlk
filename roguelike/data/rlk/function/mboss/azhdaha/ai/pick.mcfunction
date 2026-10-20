# @s = body: the weighted pick in the sampled zone (#azFront 1: the HEAD near column once, after the anti-stall).
execute if score #azFront mb matches 1 run scoreboard players set #azZone mb 1
scoreboard players set #azFront mb 0
function rlk:mboss/azhdaha/ai/pick_z
