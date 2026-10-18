# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden). The pattern goes,
# the field ends (meter, low gravity, cut). The death clip: the seam flickers out, the halo and the drill pods
# fall, the ring sinks tilted 40 degrees, then it scales out. Mechanical sounds only (deathSnd false).
# The kit: every decal goes, the banner if it still shows, every HUD flag off (meter, low gravity, hint, groggy).
function rlk:mboss/fieldgen/p/cancel
function rlk:mboss/fieldgen/fx/tele/clear
function rlk:mboss/fieldgen/hud/banner_cut
function rlk:mboss/fieldgen/fx/hud/clear
scoreboard players set #fgOpen mb 0
scoreboard players set #fgLowG mb 0
scoreboard players set #fgField mb 0
scoreboard players set #fgBrkQ mb 0
scoreboard players set #fgSt mb 7
function rlk:mboss/fieldgen/rig/prop/clear
function rlk:mboss/fieldgen/rig/play/death
function rlk:mboss/fieldgen/seq_c/death/start
