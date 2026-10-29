# Everything of the fight state stops (death, cleanup; any executor): the pattern, the mantle, a transition, tags.
function rlk:boss/tachy/core/cancel_d
function rlk:boss/tachy/mantle/cancel
execute if score #pat tk matches 54 if score #ph tk matches 3 run function rlk:boss/tachy/core/sq/t1/cancel
execute if score #pat tk matches 54 if score #ph tk matches 6 run function rlk:boss/tachy/core/sq/t2/cancel
execute if score #pat tk matches 55 run function rlk:boss/tachy/core/sq/intro/cancel
kill @e[tag=rlk_tk_p]
kill @e[tag=rlk_tk_air]
tag @e[tag=rlk_tk_core] remove rlk_tk_core
tag @e[tag=rlk_tk_mantle] remove rlk_tk_mantle
scoreboard players set #pat tk 0
scoreboard players set #stag tk 0
scoreboard players set #stun tk 0
scoreboard players set #taken tk 100
scoreboard players set #done tk 0
