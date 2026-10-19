# @s = body, positioned at the fan-out end of crescent 4 of swing 4: #bp12D44 = its dive time (from the
# straight distance to its landing point), its landing clock on the marker (mbT), the decal.
execute store result score #bp12X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44,limit=1] Pos[0] 10
summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help","rlk_mb_bf_p12h"]}
execute store result score #t mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12h,limit=1] Pos[0] 10
scoreboard players operation #bp12X mb -= #t mb
execute store result score #bp12Y mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44,limit=1] Pos[1] 10
scoreboard players add #bp12Y mb 7
execute store result score #t mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12h,limit=1] Pos[1] 10
scoreboard players operation #bp12Y mb -= #t mb
execute store result score #bp12Z mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44,limit=1] Pos[2] 10
execute store result score #t mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12h,limit=1] Pos[2] 10
scoreboard players operation #bp12Z mb -= #t mb
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12h]
scoreboard players operation #bp12X mb *= #bp12X mb
scoreboard players operation #bp12Y mb *= #bp12Y mb
scoreboard players operation #bp12Z mb *= #bp12Z mb
scoreboard players operation #bp12X mb += #bp12Y mb
scoreboard players operation #bp12X mb += #bp12Z mb
scoreboard players set #bp12D44 mb 7
execute if score #bp12X mb matches 1089.. run scoreboard players set #bp12D44 mb 8
execute if score #bp12X mb matches 1600.. run scoreboard players set #bp12D44 mb 9
execute if score #bp12X mb matches 2209.. run scoreboard players set #bp12D44 mb 10
execute if score #bp12X mb matches 2917.. run scoreboard players set #bp12D44 mb 11
execute if score #bp12X mb matches 3722.. run scoreboard players set #bp12D44 mb 12
execute if score #bp12X mb matches 4624.. run scoreboard players set #bp12D44 mb 13
execute if score #bp12X mb matches 5626.. run scoreboard players set #bp12D44 mb 14
execute if score #bp12X mb matches 6725.. run scoreboard players set #bp12D44 mb 15
execute if score #bp12X mb matches 7922.. run scoreboard players set #bp12D44 mb 16
execute if score #bp12X mb matches 9217.. run scoreboard players set #bp12D44 mb 17
execute if score #bp12X mb matches 10609.. run scoreboard players set #bp12D44 mb 18
execute if score #bp12X mb matches 12101.. run scoreboard players set #bp12D44 mb 19
execute if score #bp12X mb matches 13690.. run scoreboard players set #bp12D44 mb 20
execute if score #bp12X mb matches 15377.. run scoreboard players set #bp12D44 mb 21
execute if score #bp12X mb matches 17162.. run scoreboard players set #bp12D44 mb 22
execute if score #bp12X mb matches 19045.. run scoreboard players set #bp12D44 mb 23
execute if score #bp12X mb matches 21025.. run scoreboard players set #bp12D44 mb 24
execute if score #bp12X mb matches 23104.. run scoreboard players set #bp12D44 mb 25
execute if score #bp12X mb matches 25282.. run scoreboard players set #bp12D44 mb 26
execute if score #bp12X mb matches 27556.. run scoreboard players set #bp12D44 mb 27
execute if score #bp12X mb matches 29929.. run scoreboard players set #bp12D44 mb 28
execute if score #bp12X mb matches 32400.. run scoreboard players set #bp12D44 mb 29
execute if score #bp12X mb matches 34969.. run scoreboard players set #bp12D44 mb 30
execute if score #bp12X mb matches 37637.. run scoreboard players set #bp12D44 mb 31
execute if score #bp12X mb matches 40401.. run scoreboard players set #bp12D44 mb 32
execute if score #bp12X mb matches 43264.. run scoreboard players set #bp12D44 mb 33
execute if score #bp12X mb matches 46225.. run scoreboard players set #bp12D44 mb 34
execute if score #bp12X mb matches 49284.. run scoreboard players set #bp12D44 mb 35
execute if score #bp12X mb matches 52442.. run scoreboard players set #bp12D44 mb 36
execute if score #bp12X mb matches 55696.. run scoreboard players set #bp12D44 mb 37
execute if score #bp12X mb matches 59049.. run scoreboard players set #bp12D44 mb 38
execute if score #bp12X mb matches 62500.. run scoreboard players set #bp12D44 mb 39
execute if score #bp12X mb matches 66049.. run scoreboard players set #bp12D44 mb 40
execute if score #bp12X mb matches 69697.. run scoreboard players set #bp12D44 mb 41
execute if score #bp12X mb matches 73442.. run scoreboard players set #bp12D44 mb 42
execute if score #bp12X mb matches 77285.. run scoreboard players set #bp12D44 mb 43
execute if score #bp12X mb matches 81225.. run scoreboard players set #bp12D44 mb 44
execute if score #bp12X mb matches 85264.. run scoreboard players set #bp12D44 mb 45
execute if score #bp12X mb matches 89401.. run scoreboard players set #bp12D44 mb 46
execute if score #bp12X mb matches 93636.. run scoreboard players set #bp12D44 mb 47
execute if score #bp12X mb matches 97970.. run scoreboard players set #bp12D44 mb 48
execute if score #bp12X mb matches 102400.. run scoreboard players set #bp12D44 mb 49
execute if score #bp12X mb matches 106929.. run scoreboard players set #bp12D44 mb 50
execute if score #bp12X mb matches 111557.. run scoreboard players set #bp12D44 mb 51
execute if score #bp12X mb matches 116281.. run scoreboard players set #bp12D44 mb 52
execute if score #bp12X mb matches 121105.. run scoreboard players set #bp12D44 mb 53
execute if score #bp12X mb matches 126025.. run scoreboard players set #bp12D44 mb 54
execute if score #bp12X mb matches 131044.. run scoreboard players set #bp12D44 mb 55
execute if score #bp12X mb matches 136162.. run scoreboard players set #bp12D44 mb 56
execute if score #bp12X mb matches 141376.. run scoreboard players set #bp12D44 mb 57
execute if score #bp12X mb matches 146690.. run scoreboard players set #bp12D44 mb 58
execute if score #bp12X mb matches 152100.. run scoreboard players set #bp12D44 mb 59
execute if score #bp12X mb matches 157609.. run scoreboard players set #bp12D44 mb 60
scoreboard players operation #bp12W mb = #bp12D44 mb
scoreboard players add #bp12W mb 11
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44] mbT = #bp12W mb
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44] mbT += #bfPT mb
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t44,limit=1] run function rlk:mboss/butterfly/p/barrage/tele/pick
