# laser clock 155
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_end
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^2.392 ^2.93 rotated ~ 41 run function rlk:mboss/fieldgen/fx/p/laser_end
function rlk:mboss/fieldgen/fx/tele/mline_end {id:0}
function rlk:mboss/fieldgen/fx/tele/mline_end {id:1}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/laser_stop
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3e]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3g]
