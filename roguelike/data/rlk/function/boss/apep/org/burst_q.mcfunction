# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Any executor (the failure strike and the CS ticks): two queued organism bursts.
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_burstq,limit=2] at @s run function rlk:boss/apep/org/burst_one
