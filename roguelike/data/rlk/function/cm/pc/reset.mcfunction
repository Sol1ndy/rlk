# the attack was cleared from outside (freeze / player down -> cm/cancel set cmS 0): drop what it left behind
# frozen while overheated: the core stays exposed (and the window keeps running) until its timer ends
execute if entity @s[tag=rlk_c3_core] run return run scoreboard players set @s cmS 7
tag @s remove rlk_c2_busy
tag @s remove rlk_c2_fix
tag @s remove rlk_cmch
execute if score @s cmCd matches ..19 run scoreboard players set @s cmCd 20
