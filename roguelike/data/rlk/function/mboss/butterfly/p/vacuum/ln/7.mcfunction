# The blade's lane, 7 b from her to the wall along the locked yaw, 3 b wide: the fill reaches the
# far end as the blade does (16 t after the glint; telegraph only).
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:70,w:30,tell:16,dmg:0}
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/line {len:70,w:30,back:0,tell:16,el:7,hold:3}
