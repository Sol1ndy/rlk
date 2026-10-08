# 원소 상태 매 틱 처리 (@s = 원소 상태가 있는 몹 또는 플레이어(elAct=1), at @s)
# 예약된 격변 반응 발동 (몹). 플레이어가 맞은 반응은 player/take_damage 에서 즉시 처리됨
execute if score @s rxQ matches 1.. unless entity @s[type=minecraft:player] run function rlk:element/rx_run
# 부착 원소 감쇠
execute if score @s aFire matches 1.. run scoreboard players operation @s aFire -= @s dFire
execute if score @s aFire matches ..-1 run scoreboard players set @s aFire 0
execute if score @s aWater matches 1.. run scoreboard players operation @s aWater -= @s dWater
execute if score @s aWater matches ..-1 run scoreboard players set @s aWater 0
execute if score @s aThunder matches 1.. run scoreboard players operation @s aThunder -= @s dThunder
execute if score @s aThunder matches ..-1 run scoreboard players set @s aThunder 0
execute if score @s aIce matches 1.. run scoreboard players operation @s aIce -= @s dIce
execute if score @s aIce matches ..-1 run scoreboard players set @s aIce 0
execute if score @s aGrass matches 1.. run scoreboard players operation @s aGrass -= @s dGrass
execute if score @s aGrass matches ..-1 run scoreboard players set @s aGrass 0
execute if score @s aVoid matches 1.. run scoreboard players operation @s aVoid -= @s dVoid
execute if score @s aVoid matches ..-1 run scoreboard players set @s aVoid 0
execute if score @s rnEr matches 1.. run function rlk:element/void/er_tick
execute if score @s rnNoE matches 1.. run scoreboard players remove @s rnNoE 1
# 빙결 / 활성 / 감전 / 연소
execute if score @s frzT matches 1.. run function rlk:element/frz_tick
execute if score @s quickT matches 1.. run scoreboard players remove @s quickT 1
execute if score @s aWater matches 1.. if score @s aThunder matches 1.. run function rlk:element/ec_tick
execute unless score @s aWater matches 1.. run scoreboard players set @s ecI 0
execute unless score @s aWater matches 1.. run scoreboard players set @s lnEC 0
execute unless score @s aThunder matches 1.. run scoreboard players set @s lnEC 0
execute unless score @s aThunder matches 1.. run scoreboard players set @s ecI 0
execute if score @s burnOn matches 1 run function rlk:element/burn_tick
# 초전도(물리 피해 증가) / 부착 쿨
execute if score @s scT matches 1.. run scoreboard players remove @s scT 1
execute if score @s icdT matches 1.. run scoreboard players remove @s icdT 1
# 표시 갱신 + 남은 상태가 없으면 비활성화
function rlk:element/display
scoreboard players set @s elAct 0
execute if score @s aFire matches 1.. run scoreboard players set @s elAct 1
execute if score @s aWater matches 1.. run scoreboard players set @s elAct 1
execute if score @s aThunder matches 1.. run scoreboard players set @s elAct 1
execute if score @s aIce matches 1.. run scoreboard players set @s elAct 1
execute if score @s aGrass matches 1.. run scoreboard players set @s elAct 1
execute if score @s frzT matches 1.. run scoreboard players set @s elAct 1
execute if score @s quickT matches 1.. run scoreboard players set @s elAct 1
execute if score @s scT matches 1.. run scoreboard players set @s elAct 1
execute if score @s icdT matches 1.. run scoreboard players set @s elAct 1
execute if score @s rxQ matches 1.. run scoreboard players set @s elAct 1
execute if score @s burnOn matches 1.. run scoreboard players set @s elAct 1
execute if score @s aVoid matches 1.. run scoreboard players set @s elAct 1
execute if score @s rnEr matches 1.. run scoreboard players set @s elAct 1
execute if score @s rnNoE matches 1.. run scoreboard players set @s elAct 1
