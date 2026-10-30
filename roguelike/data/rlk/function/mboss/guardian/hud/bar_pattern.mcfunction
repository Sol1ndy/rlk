# Pattern progress against its real end (#gdPLen; not the safety cap #gdPMax), empty at the end.
scoreboard players operation #buSub bu = #gdPLen mb
scoreboard players operation #buSub bu -= #gdPT mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players operation #buSubMax bu = #gdPLen mb
scoreboard players set #buSubCol bu 8
