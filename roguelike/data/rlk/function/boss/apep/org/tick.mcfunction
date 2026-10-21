# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Any executor, once per phase-2 tick (rev/tick): every organism husk runs its kind's tick (dispatch by tag: one
# selector per kind instead of a per-organism dispatch, the command budget at the cap).
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic] at @s run function rlk:boss/apep/org/basic/tick
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nurt] at @s run function rlk:boss/apep/org/nurt/tick
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_guard] at @s run function rlk:boss/apep/org/guard/tick
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nest] at @s run function rlk:boss/apep/org/nest/tick
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_destr] at @s run function rlk:boss/apep/org/destr/tick
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_pred] at @s run function rlk:boss/apep/org/pred/tick
