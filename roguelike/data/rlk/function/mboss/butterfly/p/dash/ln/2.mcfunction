# The dash lane, 2.0 b from her toward D (telegraph only: dmg 0), 0.8 b wide, until the dash.
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:20,w:8,tell:7,dmg:0}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/line {len:20,w:8,back:0,tell:7,el:7,hold:3}
