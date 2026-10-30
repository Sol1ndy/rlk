# B3 pattern tick 30
function rlk:boss/tachy/rig/look/chest/off
execute if score #b3_dl tk matches 0..8 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:40,el:1}
execute if score #b3_dl tk matches 0..8 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:40,el:3}
execute if score #b3_dl tk matches 9..16 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:80,el:1}
execute if score #b3_dl tk matches 9..16 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:80,el:3}
execute if score #b3_dl tk matches 17..24 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:120,el:1}
execute if score #b3_dl tk matches 17..24 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:120,el:3}
function rlk:boss/tachy/fx/snd/dash
