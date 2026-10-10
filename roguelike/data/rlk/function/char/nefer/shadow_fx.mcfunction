# 그림자의 일격 (위치 = 노리는 자리): 초승달 모양 초록 궤적 + 잎
particle minecraft:dust{color:[0.2,0.55,0.15],scale:1.5} ~ ~1 ~ 0.6 0.5 0.6 0 18
particle minecraft:dust{color:[0.85,1.0,0.75],scale:0.9} ~ ~1.1 ~ 0.5 0.4 0.5 0 10
particle minecraft:composter ~ ~0.8 ~ 0.6 0.4 0.6 0 8
particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2
execute unless score #k311 snd matches 1 run function rlk:snd/f386
execute unless score #k329 snd matches 1 run function rlk:snd/f387
execute unless score #k284 snd matches 1 run function rlk:snd/f388
