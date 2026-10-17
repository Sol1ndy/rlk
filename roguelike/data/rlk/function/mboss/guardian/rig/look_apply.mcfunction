# Re-applies the stored eye/spear looks (after a respawn). @s = rig anchor.
execute if score @s gdRigEye matches 0 run function rlk:mboss/guardian/rig/eye/geo
execute if score @s gdRigEye matches 1 run function rlk:mboss/guardian/rig/eye/pyro
execute if score @s gdRigEye matches 2 run function rlk:mboss/guardian/rig/eye/hydro
execute if score @s gdRigEye matches 3 run function rlk:mboss/guardian/rig/eye/electro
execute if score @s gdRigEye matches 4 run function rlk:mboss/guardian/rig/eye/cryo
execute if score @s gdRigEye matches 5 run function rlk:mboss/guardian/rig/eye/gold
execute if score @s gdRigEye matches 6 run function rlk:mboss/guardian/rig/eye/red
execute if score @s gdRigSp matches 0 run function rlk:mboss/guardian/rig/spear/geo
execute if score @s gdRigSp matches 1 run function rlk:mboss/guardian/rig/spear/pyro
execute if score @s gdRigSp matches 2 run function rlk:mboss/guardian/rig/spear/hydro
execute if score @s gdRigSp matches 3 run function rlk:mboss/guardian/rig/spear/electro
execute if score @s gdRigSp matches 4 run function rlk:mboss/guardian/rig/spear/cryo
execute if score @s gdRigSp matches 5 run function rlk:mboss/guardian/rig/spear/gold
execute if score @s gdRigSp matches 6 run function rlk:mboss/guardian/rig/spear/red
