execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/orb/remove
execute at @s run function rlk:boss/raiden/object_vfx/break
scoreboard players operation #rdObjectId rd = @s rdObjId
execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdObjectId rd run kill @s
# An eye's armed danger circle disappears as soon as the eye is destroyed (its disk becomes the pocket).
execute if score @s rdObjKind matches 1 at @s as @e[tag=rlk_rd_hazard,distance=..0.2] run function rlk:boss/raiden/hazard/expire
execute if score @s rdObjKind matches 1 run scoreboard players remove @e[tag=rlk_raiden] rdRage 50
execute as @e[tag=rlk_raiden,scores={rdRage=..-1}] run scoreboard players set @s rdRage 0
# The single eye (id 10): 「간파했군.」 and the stun (shogun.py); a multi eye loses its glow.
execute if score @s rdObjKind matches 1 at @s run function rlk:boss/raiden/sg/eye_break
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/dome_create
# As the broken clone object, before it is removed (build_raiden_illusions.py).
execute if score @s rdObjKind matches 2 at @s run function rlk:boss/raiden/illusion/on_break
kill @s
