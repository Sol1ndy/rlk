# Circling the player at 3-5 b (0.15 b/t) until the next chain (apTok).
function rlk:boss/apep/org/pred/orbit
scoreboard players remove @s apTok 1
execute if score @s apTok matches ..0 run function rlk:boss/apep/org/pred/chain_go
