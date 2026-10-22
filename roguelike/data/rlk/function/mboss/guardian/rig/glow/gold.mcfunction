# Persistent gold outline on the whole body (until glow/off; a hit flash returns to it). @s = rig anchor.
scoreboard players set @s gdRigGl 1
execute unless score @s gdRigF matches 1.. run function rlk:mboss/guardian/rig/glow_apply
