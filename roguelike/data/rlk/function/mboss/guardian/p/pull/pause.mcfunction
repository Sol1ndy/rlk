# The fight froze (player dead or reviving; @s = body): the camera layers 0.35 b in front of the eyes would
# hang where the camera was until the resume, so they go now (later ticks only move or kill them by tag).
kill @e[tag=rlk_mb_gd_p4scr]
kill @e[tag=rlk_mb_gd_p4scn]
