# macro: e. 감쇠 속도(틱당) = 부착량 ÷ 지속시간, 지속시간 = 2.5초 × U + 7초  (1U → 9.5초, 2U → 12초)
scoreboard players set #c tmp 20
scoreboard players operation #dur tmp = #elU tmp
scoreboard players operation #dur tmp /= #c tmp
scoreboard players add #dur tmp 140
scoreboard players operation #dk tmp = #new tmp
scoreboard players operation #dk tmp /= #dur tmp
execute if score #dk tmp matches ..0 run scoreboard players set #dk tmp 1
$scoreboard players operation @s d$(e) = #dk tmp
$scoreboard players set @s a$(e) 0
