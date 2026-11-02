# Q2 the wheel bursts here (positioned at the burst point; @s any): disc(2.2) T2 plain Pyro, the
# wheel's volley group (one landing for flight + burst), strikes next tick; once.
execute if score #q2_b kn matches 1 run return 0
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzGrp mb = #q2_g kn
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:22,tell:1,dmg:43}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/q2
execute positioned ~ 201.2 ~ run function rlk:boss/arlecchino/fx/p/impact_burst {r:22,c:1}
execute positioned ~ ~ ~ run function rlk:boss/arlecchino/fx/snd/impact
kill @e[tag=rlk_kn_p_q2,tag=rlk_kn_wheel]
scoreboard players set #q2_b kn 1
