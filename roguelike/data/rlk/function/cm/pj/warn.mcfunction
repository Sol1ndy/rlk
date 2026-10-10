scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run return run kill @s
execute rotated 0 0 run function rlk:cm/pj/warn_ring
