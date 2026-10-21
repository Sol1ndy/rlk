# Called by a pattern: its dangerous part is over; with a queued transition (#apTr 1) the core ends the
# pattern here (its cancel cleans the harmless tail) and T1 starts at the next decision.
scoreboard players set #apPRel mb 1
scoreboard players set #apHudQ mb 1
execute if score #apTr mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/apep/p/cut
