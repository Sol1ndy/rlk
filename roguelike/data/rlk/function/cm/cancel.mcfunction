# 하던 공격 취소 (@s = 두뇌)
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 0
tag @s remove rlk_cmch
execute as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #cid tmp run kill @s
execute as @e[tag=rlk_cmfbh,distance=..8] if score @s cmId = #cid tmp run kill @s
execute as @e[tag=rlk_cmcbw,distance=..8] if score @s cmId = #cid tmp run function rlk:cm/cn/unaim
function rlk:cm/pose_s
