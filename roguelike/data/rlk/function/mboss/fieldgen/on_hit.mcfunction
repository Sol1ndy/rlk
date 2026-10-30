# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg #crit #sub known). Scores only.
# The break meter (plan: 20 hits replace the 3 Pneuma hits): only while the field is open (#fgOpen 1, from the
# unfold to the break or the pack-up); reaction and DoT damage (#tfm 1) and item procs (#sub itv 1) do not
# count; at most one count per 6 t (gametime: a multi-hit burst or a shotgun counts once). True damage and
# hits while untargetable never reach this hook. The module tick turns a count into the fx / HUD (#fgBrkFx)
# and the 20th into the break (#fgBrkQ).
scoreboard players set #fgFlash mb 1
execute unless score #fgOpen mb matches 1 run return 0
execute if score #fgBrk mb matches 20.. run return 0
execute if score #tfm tmp matches 1 run return 0
execute if score #sub itv matches 1 run return 0
execute store result score #fgNow mb run time query gametime
scoreboard players operation #fgNow mb -= #fgBrkT mb
execute if score #fgNow mb matches ..5 run return 0
execute store result score #fgBrkT mb run time query gametime
scoreboard players add #fgBrk mb 1
scoreboard players set #fgBrkFx mb 1
execute if score #fgBrk mb matches 20.. run scoreboard players set #fgBrkQ mb 1
