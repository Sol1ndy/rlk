# 숄더뷰에서는 진짜 플레이어(카메라)가 받은 피해는 무시한다(피격은 아바타가 받음: view/av_tick)
execute unless entity @s[tag=rlk_body] run return run effect give @s minecraft:instant_health 1 20 true
# 바닐라 피해 감지 (@s = 플레이어). 원피해 #dmgIn = 깎인 바닐라 체력 × #mobDmgMul → 바닐라 체력은 즉시 원상복구
scoreboard players operation #dmgIn tmp = #vhp100 tmp
scoreboard players operation #dmgIn tmp -= #h100 tmp
scoreboard players operation #dmgIn tmp *= #mobDmgMul tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
effect give @s minecraft:instant_health 1 20 true
execute at @s anchored eyes run function rlk:player/take_damage
