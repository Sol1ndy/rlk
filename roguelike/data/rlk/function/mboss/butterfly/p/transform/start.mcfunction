# Transformation (core service pattern 20; clip transform, @s = body, at it): the cocoon glows, the wings
# open (4), the light sphere (6: 달빛 고치 + 달빛 이슬 via p/svc), ripple rings, full spread; end 30.
function rlk:mboss/butterfly/rig/look/dendro
scoreboard players set #bfLook mb 7
function rlk:mboss/butterfly/rig/face/player
# the wings open at 4: glide inside the butterfly body disc r 16.5 first (at most 0.5 b/t;
# the wing tips must clear the wall ring, plan Q9; review fix F2)
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p20c]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p20c","rlk_mb_bf_kept"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p20c,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_b
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p20c,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p20c]
function rlk:mboss/butterfly/wx/tf/0
