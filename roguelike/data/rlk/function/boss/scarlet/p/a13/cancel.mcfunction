# A13 cancel (pause / reload / death / cleanup / tests; any executor; idempotent): its hazards, cuts, discs and
# markers; the body solid, visible, normal colours, on the floor. The banner off, the darkness lifted.
kill @e[tag=rlk_hr_p_a13]
kill @e[type=minecraft:marker,tag=rlk_hr_cut]
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/scarlet/g/reset
