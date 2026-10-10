# 사파이어 구역: 사파이어 #roomSapphire 개
scoreboard players operation @a[tag=player,limit=1] sapphire += #roomSapphire tmp
tellraw @a[tag=player] [{"text":"◇ ","color":"#5B9BF0"},{"text":"사파이어 +","color":"#5B9BF0"},{"score":{"name":"#roomSapphire","objective":"tmp"},"color":"#5B9BF0"}]
execute unless score #k17 snd matches 1 run function rlk:snd/f17
execute unless score #k18 snd matches 1 run function rlk:snd/f18
particle minecraft:glow ~ ~ ~ 0.5 0.5 0.5 0 25
function rlk:room/obj/kill_group
