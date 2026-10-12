# As the boss: the hands stop; the clap zone (8 x 8) is centred between them.
execute as @e[tag=rlk_rd_clap_l,limit=1] at @s rotated as @s positioned ^ ^ ^-4 run function rlk:boss/raiden/hazard/create {shape:7,tell:14,damage:25,life:24}
execute as @e[tag=rlk_rd_clap] run data merge entity @s {teleport_duration:0}
