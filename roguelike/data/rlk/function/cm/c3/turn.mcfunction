# 무리 공통 각도 (0.01°, @s = 무리원): (게임 시간 % 240) × 1.5° + 자리 × 360° / 무리 크기 + 무리 번호마다 다른 시작각 → #c3a
execute store result score #c3a tmp run time query gametime
scoreboard players operation #c3a tmp %= #c3c240 tmp
scoreboard players operation #c3a tmp *= #c3Orb tmp
scoreboard players operation #c3s tmp = @s c2R
scoreboard players operation #c3s tmp *= #c3c36000 tmp
execute if score @s c3N matches 1.. run scoreboard players operation #c3s tmp /= @s c3N
scoreboard players operation #c3a tmp += #c3s tmp
scoreboard players operation #c3s tmp = @s c2G
scoreboard players operation #c3s tmp *= #c3c7919 tmp
scoreboard players operation #c3a tmp += #c3s tmp
scoreboard players operation #c3a tmp %= #c3c36000 tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get #c3a tmp
