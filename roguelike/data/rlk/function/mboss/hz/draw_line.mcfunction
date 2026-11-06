# Progress bar position along the line: -back + (len + back) x progress.
scoreboard players operation #pz mb = @s mbHzR
scoreboard players operation #pz mb += @s mbHzR0
scoreboard players operation #pz mb *= #p mb
scoreboard players operation #pz mb /= #c1000 mb
scoreboard players operation #pz mb -= @s mbHzR0
execute store result storage rlk:mboss hzp.pz double 0.001 run scoreboard players get #pz mb
function rlk:mboss/hz/d/line with storage rlk:mboss hzp
