# ring_o with the ticks left (#pt 60..94).
data modify storage rlk:kn p2.dec set value {r:60,t:0}
scoreboard players set #t kn 95
scoreboard players operation #t kn -= #pt kn
execute store result storage rlk:kn p2.dec.t int 1 run scoreboard players get #t kn
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/ring_o with storage rlk:kn p2.dec
