# 잔상 한 칸(0.3칸씩, 도착점 0.4칸 안이면 끝)
particle minecraft:dust{color:[0.15,0.45,0.12],scale:1.3} ~ ~1 ~ 0.05 0.25 0.05 0 2
particle minecraft:dust{color:[0.7,0.95,0.6],scale:0.7} ~ ~1.1 ~ 0.05 0.2 0.05 0 1
scoreboard players add #sn tmp 1
execute if score #sn tmp matches ..14 unless entity @e[tag=rlk_nfmv,distance=..0.4] positioned ^ ^ ^0.3 run function rlk:char/nefer/shadow_trail
