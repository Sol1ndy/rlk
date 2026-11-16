# AI sample (@s = body, every 5 fight ticks and at each decision): the player in the body frame (mv/local, mm).
# #ai_d2 = squared distance in cm^2; #rear = 6-bit history of "behind her" (rear +-60 deg, the last 30 t); #far = ticks
# farther than 14.0 b (0 when nearer).
execute unless function rlk:mboss/mv/local run return 0
scoreboard players operation #t tk = #mbLf mb
scoreboard players operation #t tk /= #c10 tk
scoreboard players operation #t2 tk = #mbLs mb
scoreboard players operation #t2 tk /= #c10 tk
scoreboard players operation #ai_d2 tk = #t tk
scoreboard players operation #ai_d2 tk *= #t tk
scoreboard players operation #t3 tk = #t2 tk
scoreboard players operation #t3 tk *= #t2 tk
scoreboard players operation #ai_d2 tk += #t3 tk
scoreboard players operation #rear tk *= #c2 tk
scoreboard players operation #rear tk %= #c64 tk
execute if score #t tk matches ..-1 run function rlk:boss/tachy/ai/rear_bit
execute if score #ai_d2 tk matches 1960001.. run scoreboard players add #far tk 5
execute unless score #ai_d2 tk matches 1960001.. run scoreboard players set #far tk 0
execute if score #ai_d2 tk matches 302501.. run scoreboard players add #ai_oor tk 5
execute unless score #ai_d2 tk matches 302501.. run scoreboard players set #ai_oor tk 0
