# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden). The fight is
# over for the player too: 달빛 고치 / 달빛 축복 받음 off, heal orbs gone. The death clip: she staggers, the wings
# (in butterfly form) shatter into lime/opal shards, she kneels and dissolves into moonlight motes and crystal
# shards. No creature voices; the registry's deathSnd false keeps the framework roar off.
# #bfWing: the wings are shown (butterfly form, or a transformation past its open event 3, where the rig is
# already in butterfly form while #bfForm is still 1): they shatter (seq_h death; review fix S3).
scoreboard players set #bfWing mb 0
execute if score #bfForm mb matches 2 run scoreboard players set #bfWing mb 1
execute if score #bfPat mb matches 20 if score #bfPT mb matches 3.. run scoreboard players set #bfWing mb 1
function rlk:mboss/butterfly/p/cancel
function rlk:mboss/butterfly/coc/clear
function rlk:mboss/butterfly/dew/clear
scoreboard players set #bfSt mb 7
function rlk:mboss/butterfly/rig/prop/clear
function rlk:mboss/butterfly/rig/play/death
# the kit: its ground decals go (a safety net: the patterns draw none since the telegraph rule 10-20)
function rlk:mboss/butterfly/fx/tele/clear
function rlk:mboss/butterfly/seq_h/death/start
