# Resume: the live hexagram again (it stays to the end of the pattern).
scoreboard players set #aq46W mb 140
scoreboard players operation #aq46W mb -= #azPT mb
execute unless score #azPT mb matches 26..138 run return 0
data modify storage rlk:mboss az.tl set value {r:48,tell:1,el:3}
execute store result storage rlk:mboss az.tl.hold int 1 run scoreboard players get #aq46W mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:boss/azhdaha/fx/tele/hexagram_o with storage rlk:mboss az.tl
