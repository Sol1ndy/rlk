# Stop the slot pattern now (tests, death, the break, reload). Callers run rlk:mboss/lib_clear first when hazards
# must go. The pattern's cancel runs as the caller (the body when it exists): it must use selectors, not @s.
execute if score #fgPat mb matches 1.. unless score #fgPNew mb matches 1 run function rlk:mboss/fieldgen/p/cancel_d
scoreboard players set #fgPat mb 0
scoreboard players set #fgPNew mb 0
scoreboard players set #fgPEnd mb 0
scoreboard players set #fgPT mb 0
scoreboard players set #fgPRel mb 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]
kill @e[tag=rlk_mb_fg_pat]
kill @e[tag=rlk_mb_fg_fxw]
execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv
