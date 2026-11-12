# First human stretch: fight time left before the transformation (or fewer patterns).
scoreboard players operation #buSub bu = #bfHumTL mb
scoreboard players operation #buSub bu -= #bfHumT mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players operation #buSubMax bu = #bfHumTL mb
scoreboard players set #buSubCol bu 8
