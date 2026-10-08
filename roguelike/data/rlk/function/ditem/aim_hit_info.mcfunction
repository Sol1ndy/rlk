# @s = 플레이어. 설명(정보 디스플레이) 에임
# 몸(숄더뷰면 아바타)에서 8칸 안에 있는 것만
execute at @e[tag=rlk_dinfo,distance=..2.2,limit=1,sort=nearest] unless entity @e[tag=rlk_body,distance=..8] run return 0
scoreboard players set @s aimingDrop 1
execute as @e[tag=rlk_dinfo,distance=..2.2,limit=1,sort=nearest] run scoreboard players operation #aimedGid tmp = @s dgid
