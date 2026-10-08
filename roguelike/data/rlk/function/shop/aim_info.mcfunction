# @s = 플레이어, at 레이 지점. 근처 상점 이름 패널을 에임 대상으로
execute as @e[tag=rlk_shop_info,distance=..2.2,limit=1,sort=nearest] run scoreboard players operation #shopAimGid tmp = @s shopGid
