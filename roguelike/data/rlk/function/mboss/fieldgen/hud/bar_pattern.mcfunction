# Pattern progress against its real end (#fgPLen), empty at the end; Geo colour.
scoreboard players operation #buSub bu = #fgPLen mb
scoreboard players operation #buSub bu -= #fgPT mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
execute if score #buSub bu > #fgPLen mb run scoreboard players operation #buSub bu = #fgPLen mb
scoreboard players operation #buSubMax bu = #fgPLen mb
scoreboard players operation #buSubCol bu = #fgPCol mb
