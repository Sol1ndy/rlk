# A record completed (#gdRecNew = element): slot = element, enchanted spear (rig API), enchanted sweep
# (pattern 12, p56) at once: its blade slices strike 16-22 (front at 18) t later (patterns.md §8.2, wind-up tuned).
scoreboard players set #gdRecOn mb 0
scoreboard players operation #gdRecEl mb = #gdRecNew mb
scoreboard players set #gdRecNew mb 0
execute if score #gdGN mb matches 1 run scoreboard players operation #gdSlotA mb = #gdRecEl mb
execute if score #gdGN mb matches 2 run scoreboard players operation #gdSlotB mb = #gdRecEl mb
scoreboard players operation #gdSwEl mb = #gdRecEl mb
function rlk:mboss/guardian/fx/record
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/look/spear_rec
function rlk:mboss/guardian/look/eye_rec
scoreboard players set #gdGP mb 3
scoreboard players set #gdPat mb 12
scoreboard players set #gdPNew mb 1
function rlk:mboss/guardian/hud/sub_guard
