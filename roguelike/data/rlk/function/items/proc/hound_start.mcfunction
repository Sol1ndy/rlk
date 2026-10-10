kill @e[tag=rlk_hound]
summon minecraft:wolf ~ ~ ~ {Tags:["rlk_hound","rlk_pet","rlk_isn"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b}
scoreboard players operation @e[tag=rlk_isn] life = #houndDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k189 snd matches 1 run function rlk:snd/f204
