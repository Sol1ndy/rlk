# @s 의 원소 부착/상태 전부 제거
scoreboard players set @s aFire 0
scoreboard players set @s aWater 0
scoreboard players set @s aThunder 0
scoreboard players set @s aIce 0
scoreboard players set @s aGrass 0
scoreboard players set @s aVoid 0
scoreboard players set @s rnEr 0
scoreboard players set @s quickT 0
scoreboard players set @s burnOn 0
scoreboard players set @s ecI 0
scoreboard players set @s scT 0
scoreboard players set @s rxQ 0
execute if score @s frzT matches 1.. run function rlk:element/frz_end
scoreboard players set @s elAct 1
