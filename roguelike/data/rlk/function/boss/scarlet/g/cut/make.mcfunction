# {s,t,dmg,kb,n} (api.cut; @s = the pattern's executor = the body): a ghost cut (PLAN §5.3) = a quiet Electro disc hazard
# of radius CUT_R 3.2 b at the player's feet on the floor, striking t ticks later (at pattern tick s), active 2 t,
# dmg % of the base hit, knockback kb along her -> the player (kbdir 1, the marker's yaw); no outline, flash or decal.
# g/cut/tag stamps it (objective hr = s, rlk_hr_cut, the pattern tags, rlk_hr_cnt when it counts: n 1).
$scoreboard players set #g_s hr $(s)
$scoreboard players set #g_n hr $(n)
scoreboard players set #hzAct mb 2
scoreboard players set #hzEl mb 3
scoreboard players set #hzKBDir mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
$scoreboard players set #hzKB mb $(kb)
$execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet rotated ~180 0 run function rlk:mboss/hz/disc {r:32,tell:$(t),dmg:$(dmg)}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/g/cut/tag
