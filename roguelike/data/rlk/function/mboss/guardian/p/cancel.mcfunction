# Stop the slot pattern now (tests, death, reload). Callers run rlk:mboss/lib_clear first when hazards must
# go. The pattern's cancel runs as the caller (the body when it exists): it must use selectors, not @s.
execute if score #gdPat mb matches 1.. unless score #gdPNew mb matches 1 run function rlk:mboss/guardian/p/cancel_d
scoreboard players set #gdPat mb 0
scoreboard players set #gdPNew mb 0
scoreboard players set #gdPEnd mb 0
scoreboard players set #gdPT mb 0
scoreboard players set #gdPRel mb 0
scoreboard players set #mbNoLeash mb 0
execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv
execute if score #mbSt mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/guardian/rig/spear/geo
execute if score #mbSt mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/guardian/rig/glow/off
