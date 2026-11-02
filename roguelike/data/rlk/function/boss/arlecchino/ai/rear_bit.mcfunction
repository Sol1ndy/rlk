# Behind her (#t = forward cm < 0): inside +-60 deg of her back when -f x 1000 >= |s| x 577 (cot 60 deg).
scoreboard players operation #t3 kn = #t kn
scoreboard players operation #t3 kn *= #cn1000 kn
scoreboard players operation #t4 kn = #t2 kn
execute if score #t4 kn matches ..-1 run scoreboard players operation #t4 kn *= #cn1 kn
scoreboard players operation #t4 kn *= #c577 kn
execute if score #t3 kn >= #t4 kn run scoreboard players add #rear kn 1
