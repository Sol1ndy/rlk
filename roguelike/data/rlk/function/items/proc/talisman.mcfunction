# @s = 맞은 몹
execute store result score #now tmp run time query gametime
execute if score #skillDmg tmp matches 1 run scoreboard players operation @s talEnd = #now tmp
execute if score #skillDmg tmp matches 1 run scoreboard players operation @s talEnd += #talDur tmp
execute if score #skillDmg tmp matches 1 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:0.9f} ~ ~2.1 ~ 0.15 0.1 0.15 0 6
execute unless score #basic itv matches 1 run return 0
execute unless score @s talEnd > #now tmp run return 0
execute if score #talCd itv matches 1.. run return 0
scoreboard players operation #talCd itv = #talCdT tmp
execute as @a[tag=player,limit=1] run function rlk:items/proc/talisman_heal
particle minecraft:heart ~ ~1.6 ~ 0.2 0.2 0.2 0 1
