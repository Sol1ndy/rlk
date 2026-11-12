# Resume: the live round's wash and rims again with the remaining tell; the sub-line comes back on the next hud.
scoreboard players operation #aq42W mb = #aq42S mb
scoreboard players operation #aq42W mb -= #azB3T mb
scoreboard players set #aq42Dp mb -1
execute unless score #aq42W mb matches 1..48 run return 0
data modify storage rlk:mboss az.tl set value {r:280,hold:3}
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/tele/mask_wash with storage rlk:mboss az.tl
execute unless score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:0,r:32,hold:3}
execute unless score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute unless score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=0},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute if score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:0,r:28,hold:3}
execute if score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute if score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=0},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute unless score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:1,r:32,hold:3}
execute unless score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute unless score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=1},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute if score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:1,r:28,hold:3}
execute if score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute if score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=1},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute unless score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:2,r:32,hold:3}
execute unless score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute unless score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=2},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute if score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:2,r:28,hold:3}
execute if score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute if score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=2},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute unless score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:3,r:32,hold:3}
execute unless score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute unless score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=3},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute if score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:3,r:28,hold:3}
execute if score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute if score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=3},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute unless score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:4,r:32,hold:3}
execute unless score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute unless score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=4},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
execute if score #aq42J mb matches 3 run data modify storage rlk:mboss az.tl set value {id:4,r:28,hold:3}
execute if score #aq42J mb matches 3 run execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq42W mb
execute if score #aq42J mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_p42s,scores={mbS=4},limit=1] run function rlk:boss/azhdaha/fx/tele/safe_rim with storage rlk:mboss az.tl
