# As the boss: the shadow becomes the slam target (hand + 12-tick disk, radius 5).
execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:12,damage:24,life:22}
execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/rig/target_slam_spawn
kill @e[tag=rlk_rd_shadow]
