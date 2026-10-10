# @s = 조준 중인 로비 오브젝트, at @s. 좌클릭 (일반 공격으로 이어지지 않게 #shopHandled)
scoreboard players set #shopHandled tmp 1
# 한 번 누른 클릭이 두 번 들어오지 않게(0.4초)
execute if score #lobCd lob matches 1.. run return 0
scoreboard players set #lobCd lob 8
execute unless score #k72 snd matches 1 run function rlk:snd/f81
scoreboard players operation #k lob = @s lact
execute as @a[tag=player,limit=1] at @s run function rlk:lobby/act
