# 처음 접속 (@s = 플레이어)
tag @s add rlk_seen
scoreboard players set @s rlkLeave 0
execute unless score #active room matches 1 if entity @s[tag=player] run function rlk:lobby/go
