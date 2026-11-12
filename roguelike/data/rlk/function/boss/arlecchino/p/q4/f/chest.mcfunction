# The aim origin (@s = body): the rig's chest anchor (the stand-in: 2 b over her feet).
function rlk:boss/arlecchino/rig/anchor/chest
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] at @s run return run summon minecraft:marker ~ ~2 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q4","rlk_kn_q4c"]}
execute at @e[type=minecraft:marker,tag=rlk_kn_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q4","rlk_kn_q4c"]}
