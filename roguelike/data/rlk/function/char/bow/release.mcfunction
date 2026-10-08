# 발사 (@s = 플레이어, at 몸): 조준 중 좌클릭. 풀차지 전이면 물리(원소 부여 상태면 그 원소) 조준 사격, 풀차지면 캐릭터의 원소
scoreboard players operation #ct tmp = @s bowT
scoreboard players operation #bK tmp = @s bowK
function rlk:char/bow/cancel
scoreboard players set @s bowCd 6
scoreboard players set @s atkCD 6
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
scoreboard players set #aIcd tmp 0
scoreboard players set #aSub tmp 8
scoreboard players set #aLife tmp 12
execute if score #ct tmp < #bowT1 tmp run function rlk:char/bow/shot_aim
execute if score #ct tmp >= #bowT1 tmp run function rlk:char/bow/shot_full
execute anchored eyes positioned ^ ^-0.1 ^0.4 run function rlk:char/bow/spawn
tag @e[tag=rlk_arrnew] remove rlk_arrnew
playsound minecraft:entity.arrow.shoot master @a ~ ~ ~ 1.0 1.0
# 요이미야: 모아 둔 염초 화살
execute if score #charN tmp matches 2 if score #ct tmp >= #bowT1 tmp if score #bK tmp matches 1.. run function rlk:char/yoimiya/kindle_fire
