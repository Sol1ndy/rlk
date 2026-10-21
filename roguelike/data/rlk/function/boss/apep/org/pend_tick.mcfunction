# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Any executor, once per tick (T1 t116-136, phase 2): the pending spawn markers age; at 20 t the organism appears.
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn] at @s run function rlk:boss/apep/org/pend
