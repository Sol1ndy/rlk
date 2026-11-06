# P4 back spikes (plan 5 P4): bristle t0 (gold 0..22 by the clip), launch t14, points t18, landings 46/51/54/59, glow t64, bursts 76/79/82/85, end 90.
kill @e[tag=rlk_mb_az_p4]
scoreboard players set #aq4G mb 0
execute rotated as @s rotated ~ 0 positioned ^0 ^4 ^-0.2 run function rlk:boss/azhdaha/fx/p/gold_plume
function rlk:boss/azhdaha/fx/snd/spikes_bristle
