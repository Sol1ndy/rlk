# Butterfly form state: counters for the 달빛 해제 decision, butterfly hitbox.
scoreboard players set #bfForm mb 2
scoreboard players set #bfBfN mb 0
scoreboard players set #bfBfT mb 0
execute store result score #bfBfLim mb run random value 4..5
function rlk:mboss/butterfly/form/hitbox_b
