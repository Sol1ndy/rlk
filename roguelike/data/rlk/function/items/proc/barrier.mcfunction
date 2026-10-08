# @s = 플레이어. 보호막이 한도(최대 체력의 #barCap%) 아래면 #barAdd% 만큼 더한다(15초 유지)
scoreboard players operation #barCd itv = #barCdT tmp
scoreboard players operation #t1 itv = @s maxHealth
scoreboard players operation #t1 itv *= #barCap tmp
scoreboard players operation #t1 itv /= #100 tmp
execute if score @s shieldHP >= #t1 itv run return 0
scoreboard players operation #t2 itv = @s maxHealth
scoreboard players operation #t2 itv *= #barAdd tmp
scoreboard players operation #t2 itv /= #100 tmp
execute if score #t2 itv matches ..0 run scoreboard players set #t2 itv 1
scoreboard players operation @s shieldHP += #t2 itv
execute if score @s shieldHP > #t1 itv run scoreboard players operation @s shieldHP = #t1 itv
scoreboard players set @s shieldT 300
