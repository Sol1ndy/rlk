# 결정 파편 +1 (@s = 플레이어). 최대 #nvMax 개, 얻을 때마다 남은 시간 갱신
execute if score @s nvS < #nvMax tmp run scoreboard players add @s nvS 1
scoreboard players operation @s nvST = #nvDur tmp
execute unless score #k225 snd matches 1 run function rlk:snd/f249
