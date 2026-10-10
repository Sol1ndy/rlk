execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] at @s rotated as @s run function rlk:boss/raiden/illusion_cue
