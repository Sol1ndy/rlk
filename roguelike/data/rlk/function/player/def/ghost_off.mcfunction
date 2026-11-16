# ghost_on 을 되돌린다(옮겼을 때만)
execute unless score #gh cb matches 1 run return 0
scoreboard players set #gh cb 0
tag @e[tag=rlk_dgo] remove rlk_body
tag @e[tag=rlk_body_real] add rlk_body
tag @e[tag=rlk_body_real] remove rlk_body_real
