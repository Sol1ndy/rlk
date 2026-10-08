particle minecraft:dust{color:[1.0,0.93,0.65],scale:0.9} ~ ~ ~ 0 0 0 0 1
scoreboard players add #sn tmp 1
execute if score #sn tmp matches ..24 unless entity @e[tag=rlk_lnt,distance=..0.6] positioned ^ ^ ^0.3 run function rlk:element/lunar/drift_beam
