# #gain 을 #treasureGold 퍼센트 늘린다(반올림)
scoreboard players operation #t1 eng = #treasureGold tmp
scoreboard players add #t1 eng 100
scoreboard players operation #gain tmp *= #t1 eng
scoreboard players add #gain tmp 50
scoreboard players operation #gain tmp /= #100 tmp
