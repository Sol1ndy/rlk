# 닿은 곳이 목표 근처면 정상 착탄, 아니면 장애물에 막힘
scoreboard players set #sdone tmp 1
scoreboard players set #blk tmp 1
scoreboard players operation #ex tmp = #sx tmp
scoreboard players operation #ex tmp -= #ox tmp
scoreboard players operation #ey tmp = #sy tmp
scoreboard players operation #ey tmp -= #oy tmp
scoreboard players operation #ez tmp = #sz tmp
scoreboard players operation #ez tmp -= #oz tmp
execute if score #ex tmp matches -1500..1500 if score #ez tmp matches -1500..1500 if score #ey tmp matches -2000..2000 run scoreboard players set #blk tmp 0
