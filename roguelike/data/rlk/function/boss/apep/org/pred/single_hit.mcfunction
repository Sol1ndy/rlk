function rlk:boss/apep/org/pred/bite_hit
function rlk:boss/apep/om/pred/look/body/fish
function rlk:boss/apep/om/pred/look/body_x/fish
execute if score @s apSock matches 1 run return run function rlk:boss/apep/org/pred/gap_go
scoreboard players set @s apT 0
scoreboard players set @s apTok 60
