# Quick stow from where the weapon is now (sheath/tick at the end of the delay, sheath/abort).
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/mark
function rlk:char/motion/sheath/stow_marked
