# AI sample (@s = body, every 5 fight ticks and at each decision): the player in the body frame (mv/local, mm).
# #ai_d2 = squared distance in cm^2; #rear = 6-bit history of "behind her" (+-60 deg, the last 30 t); #far =
# ticks farther than 14 b (0 when nearer).
execute unless function rlk:mboss/mv/local run return 0
scoreboard players operation #t kn = #mbLf mb
scoreboard players operation #t kn /= #c10 kn
scoreboard players operation #t2 kn = #mbLs mb
scoreboard players operation #t2 kn /= #c10 kn
scoreboard players operation #ai_d2 kn = #t kn
scoreboard players operation #ai_d2 kn *= #t kn
scoreboard players operation #t3 kn = #t2 kn
scoreboard players operation #t3 kn *= #t2 kn
scoreboard players operation #ai_d2 kn += #t3 kn
scoreboard players operation #rear kn *= #c2 kn
scoreboard players operation #rear kn %= #c64 kn
execute if score #t kn matches ..-1 run function rlk:boss/arlecchino/ai/rear_bit
execute if score #ai_d2 kn matches 1960001.. run scoreboard players add #far kn 5
execute unless score #ai_d2 kn matches 1960001.. run scoreboard players set #far kn 0
