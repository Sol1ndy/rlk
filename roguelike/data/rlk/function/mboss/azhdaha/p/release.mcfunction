# Called by a pattern: its dangerous part is over: the bar hides; with a queued transition the core ends
# the pattern here (its cancel cleans the harmless tail, s2.md 15 decision 5).
scoreboard players set #azPRel mb 1
scoreboard players set #azHudQ mb 1
execute if score #azTr mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/azhdaha/p/cut
