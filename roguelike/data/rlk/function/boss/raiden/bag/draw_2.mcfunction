# As the boss: draw one move from the bag into rdPat.
function rlk:boss/raiden/bag/count_2
execute if score #rdCnt rd matches 0 run function rlk:boss/raiden/bag/fill_2
execute store result score #rdR rd run random value 0..9999
scoreboard players operation #rdR rd %= #rdCnt rd
scoreboard players add #rdR rd 1
scoreboard players set #rdPick rd 0
execute if score #rdPick rd matches 0 if score #rdB11 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB11 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 11
execute if score #rdPick rd matches 0 if score #rdB12 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB12 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 12
execute if score #rdPick rd matches 0 if score #rdB13 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB13 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 13
execute if score #rdPick rd matches 0 if score #rdB14 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB14 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 14
execute if score #rdPick rd matches 0 if score #rdB16 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB16 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 16
execute if score #rdPick rd matches 0 if score #rdB17 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB17 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 17
execute if score #rdPick rd matches 0 if score #rdB18 rd matches 1 run scoreboard players remove #rdR rd 1
execute if score #rdPick rd matches 0 if score #rdB18 rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd 18
scoreboard players operation @s rdPat = #rdPick rd
