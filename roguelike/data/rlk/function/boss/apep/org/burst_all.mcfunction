# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Every living organism bursts (a failure strike, the CS wilt; no progress): its burst fx at it, two at once,
# the rest queued (a marker each, two per tick from the service's tick: org/burst_q; perf, AP-I2: six bursts
# with the strike / wilt tick passed the 3000-commands budget).
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org,limit=2] at @s positioned ~ ~0.6 ~ run function rlk:boss/apep/fx/p/org_burst
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org,limit=2] run tag @s add rlk_mb_ap_burst
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org,tag=!rlk_mb_ap_burst] at @s run summon minecraft:marker ~ ~0.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_burstq"]}
