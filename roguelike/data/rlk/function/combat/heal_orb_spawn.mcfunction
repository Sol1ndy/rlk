# 회복구슬 소환 (@s = 몹, at @s). 위로 튀었다가 착지
execute store result storage rlk:ho mx double 0.01 run random value -18..18
execute store result storage rlk:ho mz double 0.01 run random value -18..18
function rlk:combat/heal_orb_spawn2 with storage rlk:ho
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 0.5 0.7
