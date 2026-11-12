# 1 when the player is in front of her (|bearing| <= 45 deg: f >= |s|, f > 0), else fail.
execute if score #ai_lf hr matches ..0 run return fail
scoreboard players operation #t4 hr = #ai_ls hr
execute if score #t4 hr matches ..-1 run scoreboard players operation #t4 hr *= #cn1 hr
execute if score #ai_lf hr >= #t4 hr run return 1
return fail
