# A heal of 25 % of max HP through the real path (player/heal -> items/hook/on_heal -> mboss/player_heal):
# under 달빛 고치 it is 15 % received (x 0.6), which fills the 15 % cure meter at once.
execute as @a[tag=player,limit=1] run scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp /= #c4 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
execute as @a[tag=player,limit=1] run function rlk:player/heal
