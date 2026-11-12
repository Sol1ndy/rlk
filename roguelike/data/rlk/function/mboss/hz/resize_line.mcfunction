# len = mbHzR, back = mbHzR0, width #hzSzW (tenths, 0 = keep): as hz/init_line.
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW = #hzSzW mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW *= #c100 mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzHW /= #c2 mb
execute if score #hzSzW mb matches 1.. run scoreboard players operation @s mbHzC = @s mbHzHW
execute if score #hzSzW mb matches 1.. run scoreboard players add @s mbHzHW 300
scoreboard players operation @s mbHzLo = @s mbHzR0
scoreboard players operation @s mbHzLo *= #cm1 mb
scoreboard players remove @s mbHzLo 300
scoreboard players operation @s mbHzHi = @s mbHzR
scoreboard players add @s mbHzHi 300
