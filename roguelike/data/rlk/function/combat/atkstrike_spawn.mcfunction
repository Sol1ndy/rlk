# @s = 플레이어, at = 눈앞 목표 지점. #mypid = 소유자 pid. 좌클릭 공격 감지용 작은 인터랙션
summon minecraft:interaction ~ ~ ~ {response:false,width:1.4f,height:1.4f,Tags:["atkStrike","atkStrikeNew"]}
scoreboard players operation @e[tag=atkStrikeNew,limit=1] intOwner = #mypid tmp
tag @e[tag=atkStrikeNew] remove atkStrikeNew
