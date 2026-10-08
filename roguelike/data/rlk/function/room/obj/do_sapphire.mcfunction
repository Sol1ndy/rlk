# 사파이어 구역: 사파이어 #roomSapphire 개
scoreboard players operation @a[tag=player,limit=1] sapphire += #roomSapphire tmp
tellraw @a[tag=player] [{"text":"◇ ","color":"#5B9BF0"},{"text":"사파이어 +","color":"#5B9BF0"},{"score":{"name":"#roomSapphire","objective":"tmp"},"color":"#5B9BF0"}]
playsound minecraft:block.amethyst_block.break master @a ~ ~ ~ 1 1.3
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 0.8 1.5
particle minecraft:glow ~ ~ ~ 0.5 0.5 0.5 0 25
function rlk:room/obj/kill_group
