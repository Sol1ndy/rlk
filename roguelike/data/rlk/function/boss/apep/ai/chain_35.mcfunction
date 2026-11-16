# After 생명의 나선: the chain roll ({31: 40}); the chain starts 12 t after the end (>= 20 t after
# the last hit at clock 64, plan 7.4).
execute store result score #apR mb run random value 0..99
execute if score #apR mb matches 0..39 run scoreboard players set #apChP mb 31
execute if score #apChP mb matches 1.. run scoreboard players operation #apChT mb = #apFc mb
execute if score #apChP mb matches 1.. run scoreboard players add #apChT mb 12
execute if score #apChP mb matches 1.. run scoreboard players set #apCool mb 12
