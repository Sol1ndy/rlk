# 중력 +#cgGain (#lnT = 1 달 감전 / 2 달 개화 / 3 달 결정). 종류마다 #cgTypeCd 틱(기본 1초)에 한 번
execute if score #lnT tmp matches 1 if score #cgC1 itv matches 1.. run return 0
execute if score #lnT tmp matches 2 if score #cgC2 itv matches 1.. run return 0
execute if score #lnT tmp matches 3 if score #cgC3 itv matches 1.. run return 0
execute if score #lnT tmp matches 1 run scoreboard players operation #cgC1 itv = #cgTypeCd tmp
execute if score #lnT tmp matches 2 run scoreboard players operation #cgC2 itv = #cgTypeCd tmp
execute if score #lnT tmp matches 3 run scoreboard players operation #cgC3 itv = #cgTypeCd tmp
execute if score #lnT tmp matches 1 run scoreboard players operation #cgG1 itv += #cgGain tmp
execute if score #lnT tmp matches 2 run scoreboard players operation #cgG2 itv += #cgGain tmp
execute if score #lnT tmp matches 3 run scoreboard players operation #cgG3 itv += #cgGain tmp
scoreboard players operation #cgG itv += #cgGain tmp
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] unless score #k145 snd matches 1 run function rlk:snd/f153
execute if score #cgG itv >= #cgMax tmp as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:items/proc/cg_gi
