# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden). The fight is
# over for the player too: 달빛 고치 / 달빛 축복 받음 off, heal orbs gone. The death clip: she staggers, the wings
# (in butterfly form) shatter into lime/opal shards, she kneels and dissolves into moonlight motes and crystal
# shards. No creature voices; the registry's deathSnd false keeps the framework roar off.
function rlk:mboss/butterfly/p/cancel
function rlk:mboss/butterfly/coc/clear
function rlk:mboss/butterfly/dew/clear
scoreboard players set #bfSt mb 7
function rlk:mboss/butterfly/rig_stub/prop/clear
function rlk:mboss/butterfly/rig_stub/play/death
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.2
