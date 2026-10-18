# Field opening clock 13 (@s = body): warp-out flash over the old spot (the glitch marker), untargetable,
# teleported to the arena centre facing the player (invisible until the warp-in clip).
kill @e[tag=rlk_mb_fg_fxw]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_fx","rlk_mb_fg_fxw"]}
tag @s add rlk_mb_inv
function rlk:mboss/fieldgen/u/centre
