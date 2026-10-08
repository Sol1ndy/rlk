$summon minecraft:item ~ ~0.8 ~ {Tags:["rlk_gold","rlk_sap","rlk_goldnew"],Glowing:1b,PickupDelay:32767s,Invulnerable:1b,Item:{id:"minecraft:diamond",count:1,components:{"minecraft:custom_data":{rlk_gold:1b}}},Motion:[$(mx),0.45,$(mz)]}
scoreboard players set @e[tag=rlk_goldnew] gval 1
scoreboard players set @e[tag=rlk_goldnew] life -8
tag @e[tag=rlk_goldnew] remove rlk_goldnew
