# 재사용 대기 × (1000 − 개수 × #hourglassCd‰) ÷ 1000 (최대 90% 감소)
scoreboard players operation #t1 itv = @s it_hourglass_shard
scoreboard players operation #t1 itv *= #hourglassCd tmp
scoreboard players set #t2 itv 1000
scoreboard players operation #t2 itv -= #t1 itv
execute if score #t2 itv matches ..100 run scoreboard players set #t2 itv 100
scoreboard players operation @s skillCd *= #t2 itv
scoreboard players operation @s skillCd /= #1000 tmp
