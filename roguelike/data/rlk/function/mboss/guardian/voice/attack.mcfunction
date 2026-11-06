# Attack line (K18): one of two, at most once per 20 s. Patterns call it at their cast/release tick.
execute if score #gdVoCd mb matches 1.. run return 0
scoreboard players set #gdVoCd mb 400
execute store result score #gdR mb run random value 0..1
execute if score #gdR mb matches 0 run function rlk:mboss/line/say {t:"처결하노라!",c:"#F2D488",gap:2,hold:30,snd:2}
execute if score #gdR mb matches 1 run function rlk:mboss/line/say {t:"사라져라 마땅한 존재여!",c:"#F2D488",gap:2,hold:34,snd:2}
