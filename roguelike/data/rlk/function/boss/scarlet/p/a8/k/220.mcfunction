# A8 pattern tick 220.
function rlk:boss/scarlet/shield/judge
function rlk:boss/scarlet/fx/hud/warn {on:0}
execute if score #gres hr matches 2 run function rlk:boss/scarlet/p/a8/fail
execute if score #gres hr matches 1 run scoreboard players set #done hr 1
