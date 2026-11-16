execute unless data storage rlk:room vq[0] run return 0
execute store result score #vk tmp run data get storage rlk:room vq[0]
scoreboard players set #vok tmp 1
execute if score #vk tmp matches 8 if score #mirUsed room matches 1.. run scoreboard players set #vok tmp 0
execute if score #vk tmp matches 12 if entity @a[tag=player,limit=1,scores={invCap=18..}] run scoreboard players set #vok tmp 0
execute if score #vok tmp matches 1 run data modify storage rlk:room next append from storage rlk:room vq[0]
data remove storage rlk:room vq[0]
function rlk:room/node/validate_loop
