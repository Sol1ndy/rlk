# @s = 플레이어. 페보니우스 비전: 치명타 발생 시 #favChance% 확률로 원소 에너지 #favEnergy(×100) × 원소 충전 효율 회복, 발동하면 쿨타임 #favCdT 틱
# 치명타 한 번이 여러 적에게 맞아도 판정은 한 번(같은 틱에는 한 번만)
execute store result score #now tmp run time query gametime
execute if score @s favAt = #now tmp run return 0
scoreboard players operation @s favAt = #now tmp
execute store result score #rng tmp run random value 1..100
execute if score #rng tmp > #favChance tmp run return 0
# 회복량 = #favEnergy × 원소 충전 효율% (char/energy_add) / 쿨타임 시작
scoreboard players operation #enAdd tmp = #favEnergy tmp
function rlk:char/energy_add
scoreboard players operation @s favCd = #favCdT tmp
execute at @s run playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 0.9 1.5
execute at @s run playsound minecraft:entity.breeze.charge master @s ~ ~ ~ 0.35 1.8
