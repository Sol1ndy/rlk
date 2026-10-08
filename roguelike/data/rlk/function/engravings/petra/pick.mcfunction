# @s = 주운 결정 조각. 2개: 방어막량 +#petraShield% / 4개: #petraT 틱 동안 그 원소(rxEl)로 주는 피해 증가
scoreboard players operation #t1 eng = #petraShield tmp
scoreboard players add #t1 eng 100
scoreboard players operation #amt tmp *= #t1 eng
scoreboard players operation #amt tmp /= #100 tmp
execute unless score petra engN matches 4.. run return 0
scoreboard players operation #petraEl eng = @s rxEl
scoreboard players operation #petraT eng = #petraDur tmp
