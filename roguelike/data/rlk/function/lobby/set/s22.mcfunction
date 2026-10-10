function rlk:lobby/set/cfg
execute store result score #t lob run data get storage rlk:lobby cfg.side
scoreboard players add #t lob 1
execute if score #t lob matches 2.. run scoreboard players set #t lob 0
execute store result storage rlk:lobby cfg.side int 1 run scoreboard players get #t lob
function rlk:lobby/set/cam
function rlk:lobby/set/labels
