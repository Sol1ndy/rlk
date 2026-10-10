function rlk:lobby/set/cfg
execute store result score #t lob run data get storage rlk:lobby cfg.h
scoreboard players add #t lob 1
execute if score #t lob matches 3.. run scoreboard players set #t lob 0
execute store result storage rlk:lobby cfg.h int 1 run scoreboard players get #t lob
function rlk:lobby/set/cam
function rlk:lobby/set/labels
