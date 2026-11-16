# FN-cam: @s = the released player. To the avatar's place (no avatar: a /reload or a relog removed it -> the place stored
# at the hold; view/tick then makes the new avatar there), turned to the boss as seen from the F5 seat (2.4 b up), the
# avatar turned to her too, the seat made again and the player seated at once unless they are sneaking (else
# view/ride_tick seats them: its own sneak rule). The client answers a mount with "Press <key> to Dismount" on the action
# bar (the packet goes out inside `ride`): an empty action bar right after it replaces that line in the same tick.
execute at @e[tag=rlk_av,limit=1] run tp @s ~ ~ ~
execute unless entity @e[tag=rlk_av,limit=1] if data storage rlk:mboss camret.x run function rlk:mboss/cam/ret with storage rlk:mboss camret
execute at @s positioned ~ ~2.4 ~ facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes run rotate @s ~ ~
execute as @e[tag=rlk_av,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet run rotate @s ~ 0
execute unless entity @e[tag=rlk_vseat,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:mboss/cam/seat
execute if entity @e[tag=rlk_vseat,limit=1] unless predicate rlk:in_sneak run function rlk:view/ride_mount
title @s actionbar ""
