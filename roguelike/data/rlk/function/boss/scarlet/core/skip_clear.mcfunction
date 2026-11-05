# The skip prompt off for good (the window ended, the skip, the intro end).
execute if score #skip hr matches ..-1 run return 0
function rlk:boss/scarlet/fx/hud/skip {s:5}
scoreboard players set #skip hr -1
