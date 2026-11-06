# A8 pattern tick 194.
function rlk:boss/scarlet/shield/judge
scoreboard players set #hrLook hr 2
function rlk:boss/scarlet/fx/hud/warn {on:0}
execute if score #gres hr matches 2 run function rlk:boss/scarlet/p/a8/fail
