# xc = {tk:{c,x,d,p,u}, ...} → xc = {text:"값단위", ...}
scoreboard players add #dtk tmp 1
function rlk:items/tune/fmt with storage rlk:tune xc.tk
data remove storage rlk:tune xc.tk
data modify storage rlk:tune xc.text set from storage rlk:tune ftext
