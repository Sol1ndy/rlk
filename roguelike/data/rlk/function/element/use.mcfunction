# macro: e, m(%). @s 의 부착 원소 e 를 #elU × m% 만큼 소모
$scoreboard players set #use tmp $(m)
scoreboard players operation #use tmp *= #elU tmp
scoreboard players operation #use tmp /= #100 tmp
$scoreboard players operation @s a$(e) -= #use tmp
$execute if score @s a$(e) matches ..0 run scoreboard players set @s a$(e) 0
