# 파고듦(0.3초, 아직 맞힐 수 있음) → 땅속
execute if score @s c2T matches 1.. run return 0
function rlk:cm/sb/hide
scoreboard players operation @s c2T = #c3Dn_sb tmp
