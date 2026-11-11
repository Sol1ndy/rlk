# The mannequin is hidden while its stand-in rig plays (as char/motion/hide_avatar does for the rig characters).
effect give @e[tag=rlk_av,limit=1] minecraft:invisibility infinite 0 true
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
item replace entity @e[tag=rlk_av,limit=1] weapon.offhand with minecraft:air
