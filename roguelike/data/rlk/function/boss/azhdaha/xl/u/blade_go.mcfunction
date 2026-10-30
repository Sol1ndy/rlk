# @s = a new blade prop (positioned / rotated = its flight): look, then pj/launch
# (2 b/t, life 6 t, hit radius 1.6, Hydro, the host strike group #axlBG).
tag @s remove rlk_mb_az_xnb
tp @s ~ ~ ~ ~ 0
function rlk:boss/azhdaha/fx/look {kind:"blade",col:5224703}
data merge entity @s {view_range:2f,shadow_radius:0f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.2f,1.6f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set #pjEl mb 2
scoreboard players set #pjNR mb 1
scoreboard players operation #pjGrp mb = #axlBG mb
function rlk:mboss/pj/launch {spd:20,life:6,dmg:90,hr:16}
