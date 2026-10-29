# The pattern set #done (@s = body): its G3 tag off, the post-pattern G1 swap (always after K, 50 % after a C),
# else the recovery.
tag @s remove rlk_tk_core
scoreboard players set #done tk 0
scoreboard players set #pat tk 0
scoreboard players set #pt tk 0
execute if score #last tk matches 5..7 store result score #t tk run random value 1..100
execute if score #last tk matches 5..7 if score #t tk matches ..50 run return run function rlk:boss/tachy/el/swap_start
function rlk:boss/tachy/ai/rec_start
function rlk:boss/tachy/hud/sub
