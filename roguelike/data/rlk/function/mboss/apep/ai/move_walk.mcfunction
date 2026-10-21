scoreboard players set #apMvK mb 2
scoreboard players set #apMvD mb 1
execute store result score #apR mb run random value 0..1
execute if score #apR mb matches 0 run scoreboard players set #apMvD mb -1
scoreboard players set #apPick mb 10
function rlk:mboss/apep/ai/go_raw
return 1
