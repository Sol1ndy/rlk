scoreboard players set #buSub bu 189
scoreboard players operation #buSub bu -= #apq32 mb
scoreboard players set #buSubMax bu 33
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubCol bu 8
