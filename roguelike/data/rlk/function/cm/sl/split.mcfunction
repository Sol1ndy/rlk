# 분열 (@s = 뿌리, 몸 쪽을 봄): 0°/120°/240° 방향 0.5칸(설 수 없으면 제자리)에 작은 슬라임, 살짝 바깥으로 튕김(서로 2칸 안 → 연쇄 방전)
scoreboard players set #c2PLv tmp 0
execute if score @s mlv matches 1.. run scoreboard players operation #c2PLv tmp = @s mlv
execute rotated ~ 0 run function rlk:cm/sl/kid
execute rotated ~120 0 run function rlk:cm/sl/kid
execute rotated ~240 0 run function rlk:cm/sl/kid
