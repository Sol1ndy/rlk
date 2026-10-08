# 중력 +#cgGain (#lnT = 1 달 감전 / 2 달 개화 / 3 달 결정). 종류마다 1초에 한 번
execute if score #lnT tmp matches 1 if score #cgC1 itv matches 1.. run return 0
execute if score #lnT tmp matches 2 if score #cgC2 itv matches 1.. run return 0
execute if score #lnT tmp matches 3 if score #cgC3 itv matches 1.. run return 0
execute if score #lnT tmp matches 1 run scoreboard players set #cgC1 itv 20
execute if score #lnT tmp matches 2 run scoreboard players set #cgC2 itv 20
execute if score #lnT tmp matches 3 run scoreboard players set #cgC3 itv 20
execute if score #lnT tmp matches 1 run scoreboard players operation #cgG1 itv += #cgGain tmp
execute if score #lnT tmp matches 2 run scoreboard players operation #cgG2 itv += #cgGain tmp
execute if score #lnT tmp matches 3 run scoreboard players operation #cgG3 itv += #cgGain tmp
scoreboard players operation #cgG itv += #cgGain tmp
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 0.6 0.8
execute if score #cgG itv >= #cgMax tmp as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:items/proc/cg_gi
