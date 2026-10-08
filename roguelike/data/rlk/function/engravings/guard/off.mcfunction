# 수호 4개가 아님 (@s = 플레이어): 보호막 없앰
execute unless score @s gShield matches 1.. unless score @s gCd matches 1.. run return 0
scoreboard players set @s gShield 0
scoreboard players set @s gCd 0
scoreboard players reset 수호보호막 stacks
