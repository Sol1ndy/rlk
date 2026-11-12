# P7 whip/end (Electro, plan 4.6): 3 bolt discs r 1.8 at 4 / 8 / 12 b along the end line at E+3 and a crystal
# line (hz/line len 12 w 2.4) at E+13, all one group, x_wline; the Electro strip (line len 12 w 4, 80 t, x_estrip)
# from E+15; violet arcs crawl along the tail until the bolts (body fx, the tell). Context: the end-line point,
# rotated along the end line.
function rlk:mboss/grp_new
scoreboard players operation #axtG mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 469
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #axtG mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute positioned ^ ^ ^4 run function rlk:mboss/hz/disc {r:18,tell:15,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 469
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #axtG mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute positioned ^ ^ ^8 run function rlk:mboss/hz/disc {r:18,tell:15,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 469
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #axtG mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute positioned ^ ^ ^12 run function rlk:mboss/hz/disc {r:18,tell:15,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 468
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #axtG mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
function rlk:mboss/hz/line {len:120,w:24,tell:25,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
scoreboard players set #azAftF mb 48
scoreboard players set #azAftD mb 27
function rlk:boss/azhdaha/aft/new
scoreboard players set #axtArc mb 0
function rlk:boss/azhdaha/xt/whip_end/arc
