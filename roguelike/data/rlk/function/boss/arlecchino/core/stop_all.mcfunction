# Everything of the fight state stops (death, cleanup; any executor): the pattern, a transition / replay, the stun.
function rlk:boss/arlecchino/core/cancel_d
execute if score #pat kn matches 51 run function rlk:boss/arlecchino/core/sq/t_p2/cancel
execute if score #pat kn matches 52 run function rlk:boss/arlecchino/core/sq/intro/cancel
execute if score #pat kn matches 51 run function rlk:mboss/cine/end
function rlk:boss/arlecchino/core/win_off
kill @e[tag=rlk_kn_p]
tag @e[tag=rlk_kn_stun] remove rlk_kn_stun
scoreboard players set #pat kn 0
scoreboard players set #stun kn 0
scoreboard players set #stun_t kn 0
scoreboard players set #done kn 0
