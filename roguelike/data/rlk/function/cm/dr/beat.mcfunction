# 북 한 번: 둥 소리 + 노란 파동
execute unless score #c2drbeat snd matches 1 run function rlk:cm/c2/snd/drbeat
execute unless score #c2drbeat2 snd matches 1 run function rlk:cm/c2/snd/drbeat2
execute rotated ~ 0 positioned ^ ^1.0 ^0.9 run particle minecraft:dust{color:[1.0,0.82,0.18],scale:1.6} ~ ~ ~ 0.6 0.4 0.6 0 10 normal
execute rotated ~ 0 positioned ^ ^1.0 ^0.9 run particle minecraft:electric_spark ~ ~ ~ 0.4 0.3 0.4 0.15 4 normal
