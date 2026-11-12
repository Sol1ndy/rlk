# #fgBrkLo 1 when the break comes while the closing wave_drop has the device on the floor or low in its rise
# (the pattern clock in field.W3_LOW): the rig plays break_low (same events) and the break fx follow its core.
scoreboard players set #fgBrkLo mb 0
execute if score #fgPat mb matches 21 if score #fgWvK mb matches 2 if score #fgPT mb matches 176..207 run scoreboard players set #fgBrkLo mb 1
