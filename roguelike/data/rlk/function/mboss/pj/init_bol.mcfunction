# @s = a prop launched with #pjBol mb (ar FN-1, 1..100): mbBol carries the Bond-of-Life option into mboss/hurt (hurt_bol);
# the option is spent (reset).
scoreboard players operation @s mbBol = #pjBol mb
execute if score @s mbBol matches 101.. run scoreboard players set @s mbBol 100
scoreboard players reset #pjBol mb
