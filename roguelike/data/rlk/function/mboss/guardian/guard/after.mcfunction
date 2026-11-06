# From ai/pat_done: the sweep is over. Spear back to gold, the gems keep the latest recorded element.
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/look/eye_rest
scoreboard players set #gdGP mb 4
scoreboard players set #gdT mb 0
scoreboard players set #gdGW mb 20
execute if score #gdGN mb matches 2 run scoreboard players set #gdGW mb 0
function rlk:mboss/guardian/hud/sub_guard
