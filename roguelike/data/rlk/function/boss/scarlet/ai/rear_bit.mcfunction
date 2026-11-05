# Behind her (#ai_lf < 0): inside +-60 deg of her back when -f x 1000 >= |s| x 577 (cot 60 deg).
scoreboard players operation #t3 hr = #ai_lf hr
scoreboard players operation #t3 hr *= #cn1000 hr
scoreboard players operation #t4 hr = #ai_ls hr
execute if score #t4 hr matches ..-1 run scoreboard players operation #t4 hr *= #cn1 hr
scoreboard players operation #t4 hr *= #c577 hr
execute if score #t3 hr >= #t4 hr run scoreboard players add #rear hr 1
