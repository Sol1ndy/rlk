# 빙결 (물+얼음): 두 원소를 같은 양만큼 소모하고 얼림. macro: e(붙어 있던 원소)
$scoreboard players operation #m tmp = @s a$(e)
execute if score #elU tmp < #m tmp run scoreboard players operation #m tmp = #elU tmp
$scoreboard players operation @s a$(e) -= #m tmp
# 빙결 시간(틱) = 12 + 56 × 소모량(U)   ← 원신 공식 2√(5F+4)−4 초 (F = 소모량 × 2) 의 근사
scoreboard players set #c tmp 56
scoreboard players operation #frzTicks tmp = #m tmp
scoreboard players operation #frzTicks tmp *= #c tmp
scoreboard players operation #frzTicks tmp /= #1000 tmp
scoreboard players add #frzTicks tmp 12
function rlk:element/frz_start
scoreboard players set #rx tmp 6
