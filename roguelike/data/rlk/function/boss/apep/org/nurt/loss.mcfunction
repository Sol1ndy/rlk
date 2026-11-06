# @s = the 양육 that lost a link: one link fewer, -40 % of its max HP (module mhpC); at 0 it self-destructs.
scoreboard players remove @s apSock 1
execute if score @s apSock matches ..-1 run scoreboard players set @s apSock 0
scoreboard players operation #apY mb = @s mhpM
scoreboard players set #apZ mb 40
scoreboard players operation #apY mb *= #apZ mb
scoreboard players operation #apY mb /= #c100 mb
scoreboard players operation @s mhpC -= #apY mb
function rlk:boss/apep/org/nurt/imm
execute if score @s mhpC matches ..0 run function rlk:boss/apep/org/nurt/selfd
