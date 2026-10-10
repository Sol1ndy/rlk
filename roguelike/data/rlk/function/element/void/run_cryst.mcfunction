# 공허 결정: 주우면 방어막 + 공허 잔향 (element/crystal_tick 이 줍는다)
summon minecraft:item ~ ~0.6 ~ {Tags:["rlk_crystal","rlk_rncr","rlk_cr_new"],Glowing:1b,PickupDelay:32767s,Age:-32768s,Invulnerable:1b,Item:{id:"minecraft:crying_obsidian",count:1,components:{"minecraft:custom_data":{rlk_crystal:1b}}},Motion:[0.0d,0.3d,0.0d]}
scoreboard players set @e[tag=rlk_cr_new] life 300
scoreboard players operation @e[tag=rlk_cr_new] rxDmg = #qDmg tmp
scoreboard players set @e[tag=rlk_cr_new] rxEl 5
tag @e[tag=rlk_cr_new] remove rlk_cr_new
particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.4 0.3 0.05 25
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 12
execute unless score #k59 snd matches 1 run function rlk:snd/f61
execute unless score #k20 snd matches 1 run function rlk:snd/f62
execute store result score #cc tmp if entity @e[tag=rlk_crystal]
execute if score #cc tmp matches 4.. run kill @e[tag=rlk_crystal,limit=1]
