# The rim rule: P1 (off cooldown, not the last) or the 180-degree crab-turn.
execute store result score #apR mb run random value 0..99
execute if score #apR mb matches ..49 if score #apFc mb >= #apCdE1 mb unless score #apLast mb matches 1 run return run function rlk:mboss/apep/ai/rim_p1
return run function rlk:mboss/apep/ai/turn180
