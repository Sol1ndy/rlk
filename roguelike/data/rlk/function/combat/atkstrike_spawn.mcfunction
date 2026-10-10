# @s = 플레이어, at = 눈앞 1.60 중심에서 Y -0.70. #mypid = 소유자 pid
summon minecraft:interaction ~ ~ ~ {response:false,width:1.4f,height:1.4f,Tags:["atkStrike","atkStrikeNew"]}
scoreboard players operation @e[tag=atkStrikeNew,limit=1] intOwner = #mypid tmp
tag @e[tag=atkStrikeNew] remove atkStrikeNew
