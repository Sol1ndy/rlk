# 염초 정화의 춤 (@s = 플레이어, at 몸): #yoiSkDur 틱 동안 기본 공격 화살이 불 원소 염초 화살로 바뀌고 피해가 증가한다
scoreboard players operation @s yoiSk = #yoiSkDur tmp
scoreboard players set @s yoiPcCd 0
scoreboard players set @s yoiPcN 0
playsound minecraft:item.firecharge.use master @a ~ ~ ~ 0.9 1.2
playsound minecraft:entity.firework_rocket.twinkle master @a ~ ~ ~ 0.7 1.4
particle minecraft:flame ~ ~1 ~ 0.5 0.7 0.5 0.06 40
particle minecraft:dust{color:[1.0f,0.54f,0.24f],scale:1.6f} ~ ~1 ~ 0.6 0.8 0.6 0 20
particle minecraft:firework ~ ~1.2 ~ 0.3 0.4 0.3 0.12 15
