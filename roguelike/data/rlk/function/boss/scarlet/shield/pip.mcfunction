# @s = a pip window (objective hr = its strike tick s), at its lock point. #pt = s: dashInvT 1..6; #pt = s + 1:
# dashInvT 1..5 (a dash started by s); the player's feet within 6.2 b. One pip per cut; closed after s + 1.
scoreboard players operation #t hr = @s hr
scoreboard players operation #t hr -= #pt hr
execute if score #t hr matches 1.. run return 0
execute if score #t hr matches ..-2 run return run kill @s
execute if score #pipoff hr matches 1 if score #t hr matches -1 run return run kill @s
execute if score #pipoff hr matches 1 run return 0
execute if score #t hr matches 0 if entity @a[tag=player,scores={dashInvT=1..6},limit=1] if entity @e[tag=rlk_body,limit=1,distance=..6.2] run return run function rlk:boss/scarlet/shield/take
execute if score #t hr matches -1 if entity @a[tag=player,scores={dashInvT=1..5},limit=1] if entity @e[tag=rlk_body,limit=1,distance=..6.2] run return run function rlk:boss/scarlet/shield/take
execute if score #t hr matches -1 run kill @s
