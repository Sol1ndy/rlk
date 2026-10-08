# @s = 플레이어. dbgPageCur 페이지 표시 (페이지당 12개)
execute unless score @s dbgPageCur matches 1.. run scoreboard players set @s dbgPageCur 1
execute store result score #dbgN tmp run data get storage rlk:items ids
scoreboard players set #dbgPS tmp 12
scoreboard players operation #dbgTP tmp = #dbgN tmp
scoreboard players add #dbgTP tmp 11
scoreboard players operation #dbgTP tmp /= #dbgPS tmp
execute if score @s dbgPageCur > #dbgTP tmp run scoreboard players operation @s dbgPageCur = #dbgTP tmp
scoreboard players operation #dbgStart tmp = @s dbgPageCur
scoreboard players remove #dbgStart tmp 1
scoreboard players operation #dbgStart tmp *= #dbgPS tmp
execute store result storage rlk:dbg page int 1 run scoreboard players get @s dbgPageCur
execute store result storage rlk:dbg total int 1 run scoreboard players get #dbgTP tmp
function rlk:items/debug_header with storage rlk:dbg
data modify storage rlk:dbg list set from storage rlk:items ids
scoreboard players operation #dbgSkip tmp = #dbgStart tmp
function rlk:items/debug_skip
scoreboard players operation #dbgIdx tmp = #dbgStart tmp
scoreboard players set #dbgShown tmp 0
function rlk:items/debug_loop
scoreboard players operation #dbgPrev tmp = @s dbgPageCur
scoreboard players remove #dbgPrev tmp 1
execute if score #dbgPrev tmp matches ..0 run scoreboard players set #dbgPrev tmp 1
scoreboard players operation #dbgNext tmp = @s dbgPageCur
scoreboard players add #dbgNext tmp 1
execute if score #dbgNext tmp > #dbgTP tmp run scoreboard players operation #dbgNext tmp = #dbgTP tmp
execute store result storage rlk:dbg prev int 1 run scoreboard players get #dbgPrev tmp
execute store result storage rlk:dbg next int 1 run scoreboard players get #dbgNext tmp
function rlk:items/debug_nav with storage rlk:dbg
