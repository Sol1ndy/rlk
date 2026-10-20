# @s = body (clip tick 17). T = the player now; she faces it; A = the glyph point ^-0.9 ^1.5 ^1.2 aimed at T
# (pitch 0). A 1.2 b lane from A to the arena edge (r 21) strikes at 27 for 2 t (K23; quiet,
# no ground telegraph: the glyph and the beam in the air are the tell).
kill @e[type=minecraft:marker,tag=rlk_mb_gd_p2]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p2","rlk_mb_gd_p2t"]}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p2t,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p2","rlk_mb_gd_p2a"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p2t,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #gp2Len mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/guardian/p/javelin/edge
# whole blocks (the hazard, the streak and the debris use the same length), 2..44 b
scoreboard players add #gp2Len mb 5
scoreboard players operation #gp2Len mb /= #c10 mb
scoreboard players operation #gp2Len mb *= #c10 mb
execute if score #gp2Len mb matches ..19 run scoreboard players set #gp2Len mb 20
execute if score #gp2Len mb matches 441.. run scoreboard players set #gp2Len mb 440
scoreboard players set #hzAct mb 2
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzLinger mb 4
scoreboard players set #hzQuiet mb 1
execute if score #gp2Len mb matches 20 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:20,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 30 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:30,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 40 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:40,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 50 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:50,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 60 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:60,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 70 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:70,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 80 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:80,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 90 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:90,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 100 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:100,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 110 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:110,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 120 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:120,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 130 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:130,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 140 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:140,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 150 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:150,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 160 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:160,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 170 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:170,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 180 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:180,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 190 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:190,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 200 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:200,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 210 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:210,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 220 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:220,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 230 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:230,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 240 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:240,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 250 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:250,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 260 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:260,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 270 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:270,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 280 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:280,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 290 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:290,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 300 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:300,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 310 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:310,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 320 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:320,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 330 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:330,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 340 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:340,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 350 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:350,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 360 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:360,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 370 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:370,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 380 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:380,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 390 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:390,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 400 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:400,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 410 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:410,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 420 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:420,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 430 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:430,w:12,tell:10,dmg:130}
execute if score #gp2Len mb matches 440 at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/line {len:440,w:12,tell:10,dmg:130}
function rlk:mboss/opts_reset
