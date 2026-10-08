# 클로린드 매 틱 (@s = 플레이어, at 몸)
execute if score @s clLCd matches 1.. run scoreboard players remove @s clLCd 1
execute if score @s clPcCd matches 1.. run scoreboard players remove @s clPcCd 1
execute if score @s clPT matches 1.. run scoreboard players remove @s clPT 1
execute if score @s clPT matches 0 run scoreboard players set @s clP 0
execute if score @s clBurst matches 1.. run function rlk:char/clorinde/burst_tick
scoreboard players set #clShoot tmp 0
execute if score @s clNV matches 1.. run function rlk:char/clorinde/nv_tick
execute unless score @s clNV matches 1.. run scoreboard players reset 밤순찰 stacks
# 자동 연사
execute if score @s clTg matches 1.. run scoreboard players remove @s clTg 1
execute if score @s clAuto matches 1 run function rlk:char/clorinde/auto_tick
