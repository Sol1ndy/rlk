# @s = 플레이어 (매 틱): 액션바 HUD 의 "생명의 계약 N%"(최대 체력 대비). 값이 바뀔 때만 다시 만든다
function rlk:player/bol/pct
execute if score @s bol matches 1.. if score #bolNow tmp matches ..0 run scoreboard players set #bolNow tmp 1
execute if score #bolNow tmp = @s bolKey run return 0
scoreboard players operation @s bolKey = #bolNow tmp
execute if score #bolNow tmp matches 0 run return run data modify storage rlk:hud bol set value []
execute store result storage rlk:hud bolv.n int 1 run scoreboard players get #bolNow tmp
function rlk:player/bol/hud_set with storage rlk:hud bolv
