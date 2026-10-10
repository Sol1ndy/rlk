scoreboard players operation #salonT itv = #salonDur tmp
scoreboard players set #salonI itv 0
execute at @e[tag=rlk_body,limit=1] run function rlk:items/proc/salon_spawn
execute unless score #k182 snd matches 1 run function rlk:snd/f196
execute unless score #k74 snd matches 1 run function rlk:snd/f197
