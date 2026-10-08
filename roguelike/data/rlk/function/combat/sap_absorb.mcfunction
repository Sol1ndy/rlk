# @s = 사파이어 조각. 사파이어 +gval
scoreboard players operation @a[tag=player,limit=1] sapphire += @s gval
tellraw @a[tag=player] [{"text":"◇ ","color":"#5B9BF0"},{"text":"사파이어 +","color":"#5B9BF0"},{"score":{"name":"@s","objective":"gval"},"color":"#5B9BF0"}]
execute as @a[tag=player,limit=1] at @s run playsound minecraft:block.amethyst_block.break master @s ~ ~ ~ 0.8 1.4
execute as @a[tag=player,limit=1] at @s run playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 0.6 1.5
kill @s
