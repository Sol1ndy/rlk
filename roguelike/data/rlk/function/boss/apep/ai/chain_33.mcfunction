# After 증폭의 풀: the chain roll ({36: 30}); the chain starts 3 t after the end (>= 20 t after
# the last hit at clock 96, plan 7.4).
execute store result score #apR mb run random value 0..99
execute if score #apR mb matches 0..29 run scoreboard players set #apChP mb 36
execute if score #apChP mb matches 1.. run scoreboard players operation #apChT mb = #apFc mb
execute if score #apChP mb matches 1.. run scoreboard players add #apChT mb 3
execute if score #apChP mb matches 1.. run scoreboard players set #apCool mb 3
