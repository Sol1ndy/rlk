# the attack was cleared from outside (freeze / player down -> cm/cancel set cmS 0): drop what it left behind
tag @s remove rlk_c2_busy
tag @s remove rlk_c2_fix
tag @s remove rlk_cmch
execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run kill @s
execute if score @s cmCd matches ..19 run scoreboard players set @s cmCd 20
