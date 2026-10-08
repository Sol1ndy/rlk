scoreboard players operation #t1 itv = @s it_hourglass_shard
scoreboard players operation #t1 itv *= #hourglassCd tmp
scoreboard players set #t2 itv 100
scoreboard players operation #t2 itv -= #t1 itv
execute if score #t2 itv matches ..10 run scoreboard players set #t2 itv 10
scoreboard players operation @s skillCd *= #t2 itv
scoreboard players operation @s skillCd /= #100 tmp
