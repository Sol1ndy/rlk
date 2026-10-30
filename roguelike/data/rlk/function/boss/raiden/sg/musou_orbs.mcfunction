# 8 orbs at r 21, every 45 deg from a random rotation, delivered by sky bolts.
execute store result storage rlk:rd sg.r int 1 run random value 0..44
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/sg/musou_ring with storage rlk:rd sg
