# Behind her (#t = forward cm < 0): inside +-60 deg of her back when -f x 1000 >= |s| x 577 (cot 60 deg).
scoreboard players operation #t3 tk = #t tk
scoreboard players operation #t3 tk *= #cn1000 tk
scoreboard players operation #t4 tk = #t2 tk
execute if score #t4 tk matches ..-1 run scoreboard players operation #t4 tk *= #cn1 tk
scoreboard players operation #t4 tk *= #c577 tk
execute if score #t3 tk >= #t4 tk run scoreboard players add #rear tk 1
