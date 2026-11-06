# AI sample (@s = body, every 5 fight ticks and at each decision): the player in her frame (mv/local, mm ->
# cm): #ai_lf forward, #ai_ls left, #ai_d2 = squared distance (cm^2); #rear = 6-bit history of "behind her" (+-
# 60 deg of her back); #far = ticks farther than 8 b (0 when nearer).
execute unless function rlk:mboss/mv/local run return 0
scoreboard players operation #ai_lf hr = #mbLf mb
scoreboard players operation #ai_lf hr /= #c10 hr
scoreboard players operation #ai_ls hr = #mbLs mb
scoreboard players operation #ai_ls hr /= #c10 hr
scoreboard players operation #ai_d2 hr = #ai_lf hr
scoreboard players operation #ai_d2 hr *= #ai_lf hr
scoreboard players operation #t3 hr = #ai_ls hr
scoreboard players operation #t3 hr *= #ai_ls hr
scoreboard players operation #ai_d2 hr += #t3 hr
scoreboard players operation #rear hr *= #c2 hr
scoreboard players operation #rear hr %= #c64 hr
execute if score #ai_lf hr matches ..-1 run function rlk:boss/scarlet/ai/rear_bit
execute if score #ai_d2 hr matches 640001.. run scoreboard players add #far hr 5
execute unless score #ai_d2 hr matches 640001.. run scoreboard players set #far hr 0
