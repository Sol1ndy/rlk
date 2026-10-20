# @s = a lump prop, at its target: glides there over 26 t (teleport_duration) on a
# two-segment arc (translation up 5 b over 13 t, down at the apex call).
data merge entity @s {teleport_duration:26,start_interpolation:0,interpolation_duration:13,transformation:{translation:[0f,5f,0f],scale:[1f,1f,1f]}}
tp @s ~ ~0.5 ~
