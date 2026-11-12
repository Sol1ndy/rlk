# the attack was cleared from outside (freeze / player down -> cm/cancel set cmS 0): drop what it left behind
tag @s remove rlk_c2_busy
tag @s remove rlk_c2_fix
tag @s remove rlk_cmch
execute if entity @s[tag=rlk_c3_under] run function rlk:cm/cs/surface
execute if score @s cmCd matches ..19 run scoreboard players set @s cmCd 20
