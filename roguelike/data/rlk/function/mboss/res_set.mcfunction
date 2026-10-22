# @s = a body (body_setup) with cur.res: per-element RES mbRes0..8 from the registry ("*" = the rest), tag
# rlk_mb_resel (combat/apply runs mboss/res_pre for it), mres = the physical one until the first hit.
execute store result score @s mbRes0 run data get storage rlk:mboss cur.res[0]
execute store result score @s mbRes1 run data get storage rlk:mboss cur.res[1]
execute store result score @s mbRes2 run data get storage rlk:mboss cur.res[2]
execute store result score @s mbRes3 run data get storage rlk:mboss cur.res[3]
execute store result score @s mbRes4 run data get storage rlk:mboss cur.res[4]
execute store result score @s mbRes5 run data get storage rlk:mboss cur.res[5]
execute store result score @s mbRes6 run data get storage rlk:mboss cur.res[6]
execute store result score @s mbRes7 run data get storage rlk:mboss cur.res[7]
execute store result score @s mbRes8 run data get storage rlk:mboss cur.res[8]
tag @s add rlk_mb_resel
scoreboard players operation @s mres = @s mbRes0
