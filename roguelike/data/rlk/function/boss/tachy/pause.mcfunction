# Hook pause (the fight froze): the kit cards go; patterns with a pause hook (S4).
function rlk:boss/tachy/fx/clear
execute if score #pat tk matches 8 run function rlk:boss/tachy/p/k/pause
