# @s = a new hazard made with #hzBol mb (ar FN-1, 1..100): mbBol carries the Bond-of-Life option into mboss/hurt (hurt_bol)
# or the per-mille path (hz/hurt_pm_bol); the option is spent (reset: no name stays behind).
scoreboard players operation @s mbBol = #hzBol mb
execute if score @s mbBol matches 101.. run scoreboard players set @s mbBol 100
scoreboard players reset #hzBol mb
