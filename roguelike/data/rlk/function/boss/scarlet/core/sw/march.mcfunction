# {dy} One 0.5 b step of the target line's measure (at most 64): stops within 0.45 b of the target.
execute if score #sw_n hr matches 64.. run return 0
$execute positioned ~ ~$(dy) ~ if entity @e[tag=rlk_hr_swt,distance=..0.45] run return 0
scoreboard players add #sw_n hr 1
$execute positioned ^ ^ ^0.5 run function rlk:boss/scarlet/core/sw/march {dy:"$(dy)"}
