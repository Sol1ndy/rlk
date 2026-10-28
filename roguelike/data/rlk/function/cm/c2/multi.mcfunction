# 다중 처치: 몸 위치에 묵직한 소리 + 터지는 입자 (한 번 울리면 10틱 동안은 다시 안 울림)
scoreboard players operation #c2Dq tmp = #c2Now tmp
scoreboard players operation #c2Dq tmp -= #c2Kq tmp
execute if score #c2Dq tmp matches ..10 run return 0
scoreboard players operation #c2Kq tmp = #c2Now tmp
scoreboard players add #c2Multi tmp 1
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.mace.smash_ground_heavy master @a ~ ~ ~ 1 0.8
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.crit master @a ~ ~ ~ 1 0.6
execute at @e[tag=rlk_body,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0.9 0.3 0.9 0 6 normal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:crit ~ ~1 ~ 0.8 0.5 0.8 0.6 30 normal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:electric_spark ~ ~1 ~ 0.9 0.5 0.9 0.5 20 normal
