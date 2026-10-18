# rock clock 142
function rlk:mboss/fieldgen/p/rock/rk_crumble
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/revert
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/revert
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/snd/debris_land
