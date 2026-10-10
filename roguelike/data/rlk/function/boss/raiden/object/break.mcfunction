execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/orb/remove
execute at @s run function rlk:boss/raiden/object_vfx/break
scoreboard players operation #rdObjectId rd = @s rdObjId
execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdObjectId rd run kill @s
# An eye's armed danger circle disappears as soon as the eye is destroyed.
execute if score @s rdObjKind matches 1 at @s run kill @e[tag=rlk_rd_hazard,distance=..0.2]
execute if score @s rdObjKind matches 1 run scoreboard players remove @e[tag=rlk_raiden] rdRage 50
execute as @e[tag=rlk_raiden,scores={rdRage=..-1}] run scoreboard players set @s rdRage 0
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/dome_create
# As the broken illusion object, before it is removed (build_raiden_illusions.py).
execute if score @s rdObjKind matches 2 at @s run function rlk:boss/raiden/illusion/on_break
kill @s
