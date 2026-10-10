# @s = 플레이어, 위치·방향 = 몸. 앞 1.5칸에 인형(토끼): 주변 적을 도발, 5초 뒤 또는 파괴되면 폭발
scoreboard players operation #bunnyCd itv = #bunnyCdT tmp
kill @e[tag=rlk_decoy]
kill @e[tag=rlk_decoym]
execute rotated ~ 0 positioned ^ ^ ^1.5 run summon minecraft:rabbit ~ ~0.2 ~ {Tags:["rlk_decoy","rlk_pet"],NoAI:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Glowing:1b,attributes:[{id:"minecraft:max_health",base:80d},{id:"minecraft:scale",base:1.6d},{id:"minecraft:knockback_resistance",base:1d}],Health:80f}
execute rotated ~ 0 positioned ^ ^ ^1.5 run summon minecraft:marker ~ ~0.2 ~ {Tags:["rlk_decoym"]}
scoreboard players operation @e[tag=rlk_decoym] life = #bunnyDur tmp
execute as @e[tag=rlk_decoy,limit=1] at @s run function rlk:items/proc/bunny_taunt
execute unless score #k181 snd matches 1 run function rlk:snd/f195
