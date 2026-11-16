# Every 10 t: flames over each live fire field (kit p/fire_field, its radius), the loop sound every 20 t;
# re-armed while any fire field lives.
scoreboard players set #aq33N mb 0
execute if score #azF0 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF0 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld0,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f0
execute if score #azF1 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF1 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld1,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f1
execute if score #azF2 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF2 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld2,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f2
execute if score #azF3 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF3 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld3,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f3
execute if score #azF4 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF4 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld4,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f4
execute if score #azF5 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF5 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld5,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f5
execute if score #azF6 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF6 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld6,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f6
execute if score #azF7 mb matches 1 run scoreboard players add #aq33N mb 1
execute if score #azF7 mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fld7,limit=1] run function rlk:boss/azhdaha/fx/p/fire_field with storage rlk:mboss az.f7
scoreboard players add #aq33S mb 1
execute if score #aq33S mb matches 2.. at @e[tag=rlk_body,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_fld,sort=nearest,limit=1] run function rlk:boss/azhdaha/fx/snd/fire_loop
execute if score #aq33S mb matches 2.. run scoreboard players set #aq33S mb 0
scoreboard players set #aq33A mb 0
execute if score #aq33N mb matches 1.. run function rlk:boss/azhdaha/p/firefield/amb_arm
