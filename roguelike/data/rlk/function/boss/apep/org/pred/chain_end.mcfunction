# After chain 1: one single bite 14 t after its last bite, then 12 t, then chain 2; after chain 2: a single bite every 60 t.
function rlk:boss/apep/om/pred/look/body/fish
function rlk:boss/apep/om/pred/look/body_x/fish
scoreboard players set @s apS 7
scoreboard players set @s apT 0
execute if score @s apSock matches 1 run scoreboard players set @s apTok 14
execute if score @s apSock matches 2 run scoreboard players set @s apTok 60
execute if score @s apSock matches 2 run scoreboard players set @s apSock 3
