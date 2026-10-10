# 결정: 결정 조각 생성(15초, 최대 3개). 플레이어가 닿으면 방어막
summon minecraft:item ~ ~0.6 ~ {Tags:["rlk_crystal","rlk_cr_new"],Glowing:1b,PickupDelay:32767s,Age:-32768s,Invulnerable:1b,Item:{id:"minecraft:amethyst_shard",count:1,components:{"minecraft:custom_data":{rlk_crystal:1b}}},Motion:[0.0d,0.3d,0.0d]}
scoreboard players set @e[tag=rlk_cr_new] life 300
scoreboard players operation @e[tag=rlk_cr_new] rxDmg = #qDmg tmp
scoreboard players operation @e[tag=rlk_cr_new] rxEl = #qEl tmp
tag @e[tag=rlk_cr_new] remove rlk_cr_new
# 달 결정: 월광 결정 하나
execute if score @s lnCr matches 1 run function rlk:element/lunar/drift_spawn
scoreboard players set @s lnCr 0
execute unless score #k65 snd matches 1 run function rlk:snd/f68
execute store result score #cc tmp if entity @e[tag=rlk_crystal]
execute if score #cc tmp matches 4.. run kill @e[tag=rlk_crystal,limit=1]
