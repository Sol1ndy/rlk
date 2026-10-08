# @s = 죽는 보스, at @s. 사파이어 조각을 #sapN 개 흩뿌린다
execute unless score #sapN tmp matches 1.. run return 0
execute store result storage rlk:ho mx double 0.01 run random value -20..20
execute store result storage rlk:ho mz double 0.01 run random value -20..20
function rlk:combat/sap_spawn with storage rlk:ho
scoreboard players remove #sapN tmp 1
function rlk:combat/sap_loop
