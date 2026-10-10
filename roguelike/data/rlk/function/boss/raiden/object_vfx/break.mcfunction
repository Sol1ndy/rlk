# Detached burst survives its destroyed owner for nine ticks, then disappears.
execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/flower_break
execute unless score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/object_break
