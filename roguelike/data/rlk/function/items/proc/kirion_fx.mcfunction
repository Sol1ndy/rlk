# @s = 플레이어, at @s. 변신 소리 + 나선 이펙트 타이머 시작(메시지 없음)
scoreboard players set @s kirionFxT 30
playsound minecraft:entity.wither.spawn master @a ~ ~ ~ 0.5 0.7
playsound minecraft:item.trident.thunder master @a ~ ~ ~ 0.7 0.6
playsound minecraft:block.beacon.activate master @a ~ ~ ~ 0.6 0.5
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 20
