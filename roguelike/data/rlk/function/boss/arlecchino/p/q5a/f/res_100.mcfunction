# donut_o with the ticks left (#pt 100..120).
data modify storage rlk:kn p2.dec set value {r0:60,r:150,t:0}
scoreboard players set #t kn 121
scoreboard players operation #t kn -= #pt kn
execute store result storage rlk:kn p2.dec.t int 1 run scoreboard players get #t kn
execute at @e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/donut_o with storage rlk:kn p2.dec
