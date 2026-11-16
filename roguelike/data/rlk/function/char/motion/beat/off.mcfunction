# @s = player (player/def/beat/end): the weapon glow and the body glow go, and the stand-in rig of a mannequin character
# (its clips end before the beat does; a beat that is cut - death, the selection space, a cutscene, the next beat - removes it).
function rlk:char/motion/beat/wglow_off
function rlk:char/motion/beat/tint_off
execute if score @s plActive matches 1 run function rlk:char/motion/lite/stop
