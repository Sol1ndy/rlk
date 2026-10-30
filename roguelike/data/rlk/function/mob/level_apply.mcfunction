# @s = 몹: 최대 체력(mhpM) = mhp0(1레벨 체력) × (100 + #mobLvHp·x + #mobLvHp2·x²/100)% × #mobHpMul% (x = 레벨 - 1) 로 다시 계산하고 가득 채움. 상한 없음
scoreboard players operation #mlx tmp = @s mlv
scoreboard players remove #mlx tmp 1
scoreboard players operation #mlq tmp = #mlx tmp
scoreboard players operation #mlq tmp *= #mlx tmp
scoreboard players operation #mlq tmp *= #mobLvHp2 tmp
scoreboard players operation #mlq tmp /= #100 tmp
scoreboard players operation #mlh tmp = #mlx tmp
scoreboard players operation #mlh tmp *= #mobLvHp tmp
scoreboard players add #mlh tmp 100
scoreboard players operation #mlh tmp += #mlq tmp
scoreboard players operation #mlh tmp *= @s mhp0
scoreboard players operation #mlh tmp /= #100 tmp
# 전체 배율(#mobHpMul%)
scoreboard players operation #mlh tmp *= #mobHpMul tmp
scoreboard players operation #mlh tmp /= #100 tmp
execute if score #mlh tmp matches ..0 run scoreboard players set #mlh tmp 1
scoreboard players operation @s mhpM = #mlh tmp
scoreboard players operation @s mhpC = #mlh tmp
function rlk:mob/vhp_pin
