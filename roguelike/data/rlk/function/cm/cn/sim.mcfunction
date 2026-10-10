# (@s = 숨긴 포탄, arc 직후) 실제 비행과 똑같은 계산으로 미리 날려 봄 → #blk 1 = 목표 근처(가로 1.5칸·세로 2칸)에 닿기 전에 막힘
scoreboard players operation #sx tmp = @s cmPx
scoreboard players operation #sy tmp = @s cmPy
scoreboard players operation #sz tmp = @s cmPz
scoreboard players operation #svx tmp = @s cmVx
scoreboard players operation #svy tmp = @s cmVy
scoreboard players operation #svz tmp = @s cmVz
scoreboard players operation #ox tmp = @s cmPx
scoreboard players operation #ox tmp += #tx tmp
scoreboard players operation #oy tmp = @s cmPy
scoreboard players operation #oy tmp += #ty tmp
scoreboard players operation #oz tmp = @s cmPz
scoreboard players operation #oz tmp += #tz tmp
scoreboard players set #blk tmp 0
scoreboard players set #sdone tmp 0
scoreboard players operation #sn tmp = #n tmp
scoreboard players add #sn tmp 12
summon minecraft:marker ~ ~ ~ {Tags:["rlk_cmprobe"]}
execute as @e[tag=rlk_cmprobe,limit=1] run function rlk:cm/cn/sim_t
kill @e[tag=rlk_cmprobe]
