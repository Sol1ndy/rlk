# 부착 쿨 (@s = 맞는 대상). 타이머(50틱)가 끝났으면 부착 + 타이머 시작, 아니면 3타째마다 부착
execute unless score @s icdT matches 1.. run return run function rlk:element/icd_reset
scoreboard players add @s icdC 1
execute if score @s icdC matches 3.. run return run scoreboard players set @s icdC 0
scoreboard players set #apply tmp 0
