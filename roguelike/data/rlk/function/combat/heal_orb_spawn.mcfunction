# 회복구슬 소환 (@s = 몹, at @s). 위로 튀었다가 착지
execute store result storage rlk:ho mx double 0.01 run random value -18..18
execute store result storage rlk:ho mz double 0.01 run random value -18..18
function rlk:combat/heal_orb_spawn2 with storage rlk:ho
execute unless score #k14 snd matches 1 run function rlk:snd/f31
