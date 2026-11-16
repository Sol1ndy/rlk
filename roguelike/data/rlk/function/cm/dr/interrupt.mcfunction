# 맞으면 북 멈춤 #c2DrI 틱(2초). 가속은 다음 c2/world 에서 바로 풀림
scoreboard players operation @s c2T2 = #c2DrI tmp
tag @s remove rlk_dr_drum
execute unless score #c2drstop snd matches 1 run function rlk:cm/c2/snd/drstop
