# The stun is over (@s = body): the Banquet schedule restarts from here, the recovery.
tag @s remove rlk_kn_stun
scoreboard players set #stun kn 0
scoreboard players set #stun_t kn 0
scoreboard players set #pat kn 0
scoreboard players set #pt kn 0
execute if score #brk kn matches 10 run function rlk:boss/arlecchino/ai/resched_f
execute if score #brk kn matches 46 run function rlk:boss/arlecchino/ai/resched_q5
execute if score #brk kn matches 47 run function rlk:boss/arlecchino/ai/resched_q5
scoreboard players set #brk kn 0
function rlk:boss/arlecchino/ai/rec_start
function rlk:boss/arlecchino/hud/sub
