# W1 one tick (@s = body).
execute if score #pt tk matches 6 if score #core tk matches 0 unless entity @s[tag=rlk_tk_mantle] run tag @s add rlk_tk_core
execute if score #pt tk matches 40 run tag @s remove rlk_tk_core
function rlk:boss/tachy/p/w1/tick
