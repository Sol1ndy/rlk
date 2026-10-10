# @s = 사파이어 조각. 사파이어 +gval
scoreboard players operation @a[tag=player,limit=1] sapphire += @s gval
tellraw @a[tag=player] [{"text":"◇ ","color":"#5B9BF0"},{"text":"사파이어 +","color":"#5B9BF0"},{"score":{"name":"@s","objective":"gval"},"color":"#5B9BF0"}]
execute as @a[tag=player,limit=1] at @s unless score #k28 snd matches 1 run function rlk:snd/f28
execute as @a[tag=player,limit=1] at @s unless score #k18 snd matches 1 run function rlk:snd/f29
kill @s
