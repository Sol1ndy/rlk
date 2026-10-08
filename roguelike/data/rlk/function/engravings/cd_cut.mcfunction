# @s = 플레이어. 원소전투 스킬 재사용 대기를 #cut eng 틱 줄인다
execute unless score @s skillCd matches 1.. run return 0
scoreboard players operation @s skillCd -= #cut eng
execute if score @s skillCd matches ..-1 run scoreboard players set @s skillCd 0
