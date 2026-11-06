# The HP < 50 % triple front of the 3rd wave by hand.
scoreboard players set #fgX mb 1
execute if score #fgTri mb matches 1 run scoreboard players set #fgX mb 0
scoreboard players operation #fgTri mb = #fgX mb
execute if score #fgTri mb matches 1 run tellraw @a[tag=player] {text:"[테스트] 세 겹 충격파 켬",color:"gray"}
execute if score #fgTri mb matches 0 run tellraw @a[tag=player] {text:"[테스트] 세 겹 충격파 끔",color:"gray"}
