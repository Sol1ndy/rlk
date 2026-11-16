# Internal: the crimson glow (BoL tells) on both scythes, or none.
execute if score @s knRigGl matches 1 run data merge entity 524c4b4d-4b4e-4100-8000-00000000000a {Glowing:1b,glow_color_override:14692410}
execute if score @s knRigGl matches 1 run data merge entity 524c4b4d-4b4e-4100-8000-00000000000b {Glowing:1b,glow_color_override:14692410}
execute unless score @s knRigGl matches 1 run data merge entity 524c4b4d-4b4e-4100-8000-00000000000a {Glowing:0b}
execute unless score @s knRigGl matches 1 run data merge entity 524c4b4d-4b4e-4100-8000-00000000000b {Glowing:0b}
