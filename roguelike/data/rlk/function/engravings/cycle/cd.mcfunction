scoreboard players set #t1 eng 100
scoreboard players operation #t1 eng -= #cycleCd tmp
scoreboard players operation @s skillCd *= #t1 eng
scoreboard players operation @s skillCd /= #100 tmp
