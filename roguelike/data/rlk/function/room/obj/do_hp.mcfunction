# 생명력 구역: 최대 체력 +#hpNodePct % (런 동안 유지, items/stat_light 의 hpPct 에 더해짐)
execute as @a[tag=player,limit=1] run scoreboard players operation @s nodeHp += #hpNodePct tmp
tellraw @a[tag=player] [{"text":"❤ ","color":"#E06A8A"},{"text":"최대 체력 +","color":"#E06A8A"},{"score":{"name":"#hpNodePct","objective":"tmp"},"color":"#E06A8A"},{"text":"%","color":"#E06A8A"}]
execute unless score #k17 snd matches 1 run function rlk:snd/f17
execute unless score #k18 snd matches 1 run function rlk:snd/f18
particle minecraft:heart ~ ~ ~ 0.5 0.5 0.5 0 8
function rlk:room/obj/kill_group
