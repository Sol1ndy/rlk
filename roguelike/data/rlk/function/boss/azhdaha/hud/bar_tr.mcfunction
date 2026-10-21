scoreboard players operation #buSub bu = #azPT mb
scoreboard players operation #buSubMax bu = #azPLen mb
execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubCol bu 8
