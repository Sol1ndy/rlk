# 다시 접속 (@s = 플레이어): 런 중이 아니면 로비로
scoreboard players set @s rlkLeave 0
execute unless score #active room matches 1 if entity @s[tag=player] run function rlk:lobby/go
