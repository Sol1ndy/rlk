execute as @e[tag=rlk_rd_object,scores={rdObjKind=4,rdObjId=1}] at @s run function rlk:boss/raiden/hazard/create {shape:11,tell:12,damage:14,life:75}
execute as @e[tag=rlk_rd_object,scores={rdObjKind=4,rdObjId=1}] at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
