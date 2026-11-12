# (reload, after fld/remake) the re-made hail discs (45's; the P7 hail strip is a line) get the tag
# again and the ambience chain restarts.
scoreboard players set #aq45H mb 0
execute if score #azF0 mb matches 2 if data storage rlk:mboss az.f0{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld0] add rlk_mb_az_p45h
execute if score #azF1 mb matches 2 if data storage rlk:mboss az.f1{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld1] add rlk_mb_az_p45h
execute if score #azF2 mb matches 2 if data storage rlk:mboss az.f2{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld2] add rlk_mb_az_p45h
execute if score #azF3 mb matches 2 if data storage rlk:mboss az.f3{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld3] add rlk_mb_az_p45h
execute if score #azF4 mb matches 2 if data storage rlk:mboss az.f4{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld4] add rlk_mb_az_p45h
execute if score #azF5 mb matches 2 if data storage rlk:mboss az.f5{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld5] add rlk_mb_az_p45h
execute if score #azF6 mb matches 2 if data storage rlk:mboss az.f6{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld6] add rlk_mb_az_p45h
execute if score #azF7 mb matches 2 if data storage rlk:mboss az.f7{sh:0} run tag @e[type=minecraft:marker,tag=rlk_mb_az_fld7] add rlk_mb_az_p45h
execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_p45h,limit=1] run function rlk:boss/azhdaha/p/icespike/hail_go
