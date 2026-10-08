# 위치 = 화살. 종류별 꼬리
execute if score @s aKind matches 3..5 run particle minecraft:flame ~ ~ ~ 0.03 0.03 0.03 0.005 2
execute if score @s aKind matches 3 run particle minecraft:small_flame ^ ^ ^-1 0.05 0.05 0.05 0.01 2
execute if score @s aKind matches 1..2 run particle minecraft:crit ~ ~ ~ 0 0 0 0 1
execute if score @s aKind matches 6 run particle minecraft:firework ~ ~ ~ 0.15 0.15 0.15 0.06 8
execute if score @s aKind matches 6 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.03 6
# 기본 공격 화살: 반짝이 / 콤보 마지막 화살은 더 많이
execute if score @s aKind matches 1 run particle minecraft:firework ~ ~ ~ 0 0 0 0 1
execute if score @s aKind matches 5 run particle minecraft:firework ~ ~ ~ 0.02 0.02 0.02 0.01 1
execute if entity @s[tag=rlk_arrfin] run particle minecraft:firework ~ ~ ~ 0.06 0.06 0.06 0.03 4
