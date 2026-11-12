# Ends the glow look (the outline goes unless a hit flash is showing; flash_off then clears it). @s = rig anchor.
scoreboard players set @s gdRigGl 0
execute unless score @s gdRigF matches 1.. run function rlk:mboss/guardian/rig/glow_apply
