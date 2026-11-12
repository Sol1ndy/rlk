# @s = entity to move (body, prop, aux), positioned at the destination: straight glide over t ticks.
function rlk:mboss/mv/setup
$scoreboard players set @s mbMvN $(t)
scoreboard players set @s mbMvH 0
