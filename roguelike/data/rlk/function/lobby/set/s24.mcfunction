execute store result score #t lob run data get storage rlk:view opt.smooth
scoreboard players add #t lob 1
execute if score #t lob matches 4.. run scoreboard players set #t lob 0
execute store result storage rlk:view opt.smooth int 1 run scoreboard players get #t lob
function rlk:view/tune_apply
function rlk:lobby/set/labels
