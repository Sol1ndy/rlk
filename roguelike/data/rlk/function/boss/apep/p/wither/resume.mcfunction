# Resume (the pause cleared the kit telegraphs): the disc again with the ticks left to the strike (fill) or of the
# active window (hold).
execute if score #apPT mb matches 16..39 run scoreboard players set #apq4R mb 40
execute if score #apPT mb matches 16..39 run scoreboard players operation #apq4R mb -= #apPT mb
execute if score #apPT mb matches 16..39 store result storage rlk:mboss ap.p4.t int 1 run scoreboard players get #apq4R mb
execute if score #apPT mb matches 16..39 run data modify storage rlk:mboss ap.p4.h set value 31
execute if score #apPT mb matches 40..70 run data modify storage rlk:mboss ap.p4.t set value 1
execute if score #apPT mb matches 40..70 run scoreboard players set #apq4R mb 71
execute if score #apPT mb matches 40..70 run scoreboard players operation #apq4R mb -= #apPT mb
execute if score #apPT mb matches 40..70 store result storage rlk:mboss ap.p4.h int 1 run scoreboard players get #apq4R mb
execute if score #apPT mb matches 16..70 at @e[type=minecraft:marker,tag=rlk_mb_ap_p4d,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p4d,limit=1] run function rlk:boss/apep/p/wither/disc with storage rlk:mboss ap.p4
