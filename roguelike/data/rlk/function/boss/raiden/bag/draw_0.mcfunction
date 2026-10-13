# As the boss: draw one move from the bag into rdPat.
function rlk:boss/raiden/bag/count_0
execute if score #rdCnt rd matches 0 run function rlk:boss/raiden/bag/fill_0
execute store result score #rdR rd run random value 0..9999
scoreboard players operation #rdR rd %= #rdCnt rd
scoreboard players add #rdR rd 1
scoreboard players set #rdPick rd 0
execute if score #rdPick rd matches 0 if score #rdB1 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB1 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 1
execute if score #rdPick rd matches 0 if score #rdB2 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB2 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 2
execute if score #rdPick rd matches 0 if score #rdB3 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB3 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 3
execute if score #rdPick rd matches 0 if score #rdB4 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB4 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 4
execute if score #rdPick rd matches 0 if score #rdB5 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB5 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 5
execute if score #rdPick rd matches 0 if score #rdB6 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB6 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 6
execute if score #rdPick rd matches 0 if score #rdB7 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB7 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 7
scoreboard players operation @s rdPat = #rdPick rd
