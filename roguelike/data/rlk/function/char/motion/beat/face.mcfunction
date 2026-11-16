# The beat clip's heading: toward the attacker (tag rlk_bt_atk) when there is one (the lunge goes at it, the handspring lands
# facing it); the clip's yaw is locked on its basis marker.
execute unless entity @e[tag=rlk_bt_atk,limit=1] run return 0
execute as @e[tag=rlk_pm_basis,limit=1] at @s facing entity @e[tag=rlk_bt_atk,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
