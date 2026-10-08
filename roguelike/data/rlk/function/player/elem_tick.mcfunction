# 플레이어 원소 처리 (@s = 플레이어, 매 틱. health_tick 뒤에 호출)
scoreboard players set @s hurtElem 0
scoreboard players set @s hurtLv 0
execute if score @s infuseT matches 1.. run scoreboard players remove @s infuseT 1
execute if score @s infuseT matches 0 if score @s infuse matches 1.. run function rlk:element/infuse_end
execute if score @s shieldT matches 1.. run scoreboard players remove @s shieldT 1
execute if score @s shieldT matches 0 if score @s shieldHP matches 1.. run scoreboard players set @s shieldHP 0
execute if score @s elAct matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:element/tick
