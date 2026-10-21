scoreboard players operation #buSub bu = #apPT mb
scoreboard players operation #buSubMax bu = #apPLen mb
execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubCol bu 5
