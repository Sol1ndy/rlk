# Pattern progress against its real end (#bfPLen), empty at the end; colour = its element.
scoreboard players operation #buSub bu = #bfPLen mb
scoreboard players operation #buSub bu -= #bfPT mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
execute if score #buSub bu > #bfPLen mb run scoreboard players operation #buSub bu = #bfPLen mb
scoreboard players operation #buSubMax bu = #bfPLen mb
scoreboard players operation #buSubCol bu = #bfPCol mb
