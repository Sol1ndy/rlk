# 결정 파편 +1 (@s = 플레이어). 최대 #nvMax 개, 얻을 때마다 남은 시간 갱신
execute if score @s nvS < #nvMax tmp run scoreboard players add @s nvS 1
scoreboard players operation @s nvST = #nvDur tmp
playsound minecraft:block.amethyst_cluster.place master @s ~ ~ ~ 0.6 1.4
