# @s = 플레이어, at = 눈앞 0.30 중심에서 Y -0.16. #mypid = 소유자 pid
summon minecraft:interaction ~ ~ ~ {response:false,width:0.32f,height:0.32f,Tags:["atkBlock","atkBlockNew"]}
scoreboard players operation @e[tag=atkBlockNew,limit=1] intOwner = #mypid tmp
tag @e[tag=atkBlockNew] remove atkBlockNew
