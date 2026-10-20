# P7 whip/sweep (Cryo, plan 4.6): four ice-wall pieces on the swept arc (annular sectors r 5-12 about the tail
# root), erupting 2 t behind the tail at E+2 / 4 / 6 / 8, one own group, x_wall + a stack; a hail strip (line
# len 7 w 3.5, 60 t) on the band where the sweep ends follows the last piece (s2.md 15 decision 8). Context: the
# tail root at E, rotated as the anchor's start yaw; the pieces come from the manifest track x yaw schedule.
function rlk:mboss/grp_new
scoreboard players operation #axtG mb = #mbGrp mb
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches 1 positioned ^0.961 ^ ^0.572 rotated ~194.05 0 run function rlk:mboss/hz/sector {r:120,a:17,tell:14,dmg:80}
execute if score #azCtxSide mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches 1 positioned ^2.475 ^ ^2.576 rotated ~228.17 0 run function rlk:mboss/hz/sector {r:120,a:20,tell:16,dmg:80}
execute if score #azCtxSide mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches 1 positioned ^2.789 ^ ^4.821 rotated ~261.99 0 run function rlk:mboss/hz/sector {r:120,a:16,tell:18,dmg:80}
execute if score #azCtxSide mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches 1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches 1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches 1 positioned ^2.461 ^ ^6.127 rotated ~285.06 0 run function rlk:mboss/hz/sector {r:120,a:10,tell:20,dmg:80}
execute if score #azCtxSide mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches 1 run scoreboard players set #azAftF mb 21
execute if score #azCtxSide mb matches 1 run scoreboard players set #azAftD mb 20
execute if score #azCtxSide mb matches 1 positioned ^2.406 ^ ^6.256 rotated ~293.14 0 positioned ^ ^ ^5 run function rlk:mboss/azhdaha/aft/new
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches -1 positioned ^-0.961 ^ ^0.572 rotated ~-194.05 0 run function rlk:mboss/hz/sector {r:120,a:17,tell:14,dmg:80}
execute if score #azCtxSide mb matches -1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches -1 positioned ^-2.475 ^ ^2.576 rotated ~-228.17 0 run function rlk:mboss/hz/sector {r:120,a:20,tell:16,dmg:80}
execute if score #azCtxSide mb matches -1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches -1 positioned ^-2.789 ^ ^4.821 rotated ~-261.99 0 run function rlk:mboss/hz/sector {r:120,a:16,tell:18,dmg:80}
execute if score #azCtxSide mb matches -1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzKB mb 3
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzSfx mb 0
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzVis mb 459
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzQuiet mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzNR mb 1
execute if score #azCtxSide mb matches -1 run scoreboard players set #hzR0 mb 50
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzGrp mb = #axtG mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #hzEl mb = #azET mb
execute if score #azCtxSide mb matches -1 run scoreboard players operation #pjEl mb = #azET mb
execute if score #azCtxSide mb matches -1 positioned ^-2.461 ^ ^6.127 rotated ~-285.06 0 run function rlk:mboss/hz/sector {r:120,a:10,tell:20,dmg:80}
execute if score #azCtxSide mb matches -1 run execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute if score #azCtxSide mb matches -1 run scoreboard players set #azAftF mb 21
execute if score #azCtxSide mb matches -1 run scoreboard players set #azAftD mb 20
execute if score #azCtxSide mb matches -1 positioned ^-2.406 ^ ^6.256 rotated ~-293.14 0 positioned ^ ^ ^5 run function rlk:mboss/azhdaha/aft/new
