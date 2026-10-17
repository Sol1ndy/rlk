# P4 cancel (any executor): every entity of the pattern carries rlk_mb_gd_p4 (cage, cubes, crescents, ring
# decals); the pull point and hazards go with lib_clear; the screen overlay ends if it runs.
kill @e[tag=rlk_mb_gd_p4]
execute if score #gdPT mb matches 22..38 run function rlk:mboss/guardian/p/pull/scr_end
scoreboard players set #gp4Ok mb 0
