# The blade's lane, 39 b from her to the wall along the locked yaw, 3 b wide: the fill reaches the
# far end as the blade does (59 t after the glint; telegraph only).
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:390,w:30,tell:59,dmg:0}
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/line {len:390,w:30,back:0,tell:59,el:7,hold:3}
