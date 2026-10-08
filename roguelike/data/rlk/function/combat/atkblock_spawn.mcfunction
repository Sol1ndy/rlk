# @s = 플레이어, at = 목표 지점. #mypid = 소유자 pid
summon minecraft:interaction ~ ~ ~ {response:false,width:5f,height:3f,Tags:["atkBlock","atkBlockNew"]}
scoreboard players operation @e[tag=atkBlockNew,limit=1] intOwner = #mypid tmp
tag @e[tag=atkBlockNew] remove atkBlockNew
