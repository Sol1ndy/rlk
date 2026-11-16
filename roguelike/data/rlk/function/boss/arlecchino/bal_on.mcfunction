# @s = body: the running pattern goes (like the break, without its damage), then her stun for the balance clock.
execute if score #pat kn matches 1..49 run function rlk:boss/arlecchino/core/cancel_d
function rlk:boss/arlecchino/core/win_off
scoreboard players set #pat kn 0
scoreboard players set #done kn 0
scoreboard players set #brk kn 0
function rlk:boss/arlecchino/core/stun_start
scoreboard players set #stun_t kn 100
