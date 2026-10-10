# @s = 플레이어 (피격 처리 중). 수호 보호막이 #dmgIn 을 먼저 막는다. 깨지면 재생 대기 시작
execute unless score @s gShield matches 1.. run return 0
execute unless score #dmgIn tmp matches 1.. run return 0
scoreboard players operation #ab tmp = @s gShield
execute if score #dmgIn tmp < #ab tmp run scoreboard players operation #ab tmp = #dmgIn tmp
scoreboard players operation @s gShield -= #ab tmp
scoreboard players operation #dmgIn tmp -= #ab tmp
execute unless score #k214 snd matches 1 run function rlk:snd/f237
execute if score @s gShield matches 1.. run return 0
scoreboard players operation @s gCd = #guardCdT tmp
execute unless score #k215 snd matches 1 run function rlk:snd/f238
particle minecraft:dust{color:[0.44f,0.69f,1.0f],scale:1.2f} ~ ~ ~ 0.5 0.6 0.5 0 25
