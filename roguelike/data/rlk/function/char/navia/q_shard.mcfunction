# 포격이 맞음 (@s = 플레이어): 결정 파편 +1, #nvQSh 틱마다 한 번
execute if score @s nvQS matches 1.. run return 0
scoreboard players operation @s nvQS = #nvQSh tmp
function rlk:char/navia/shard_gain
