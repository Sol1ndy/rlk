# 바닥 물결 (@s = 구역 표식, at @s, 매 틱): 중심(wx, wz)에서 반지름 wr 의 정사각형까지를 어두운 타일로. 틱마다 #waveSpeed 칸씩 넓어짐
scoreboard players operation @s wr += #waveSpeed tmp
execute store result score #wx0 tmp run data get entity @s data.x0
execute store result score #wx1 tmp run data get entity @s data.x1
execute store result score #wz0 tmp run data get entity @s data.z0
execute store result score #wz1 tmp run data get entity @s data.z1
# 이번 틱의 범위(구역 밖으로는 나가지 않게 자름)
scoreboard players operation #ax0 tmp = @s wx
scoreboard players operation #ax0 tmp -= @s wr
scoreboard players operation #ax0 tmp > #wx0 tmp
scoreboard players operation #ax1 tmp = @s wx
scoreboard players operation #ax1 tmp += @s wr
scoreboard players operation #ax1 tmp < #wx1 tmp
scoreboard players operation #az0 tmp = @s wz
scoreboard players operation #az0 tmp -= @s wr
scoreboard players operation #az0 tmp > #wz0 tmp
scoreboard players operation #az1 tmp = @s wz
scoreboard players operation #az1 tmp += @s wr
scoreboard players operation #az1 tmp < #wz1 tmp
# 구역의 칸마다 잘라서 바꾼다(ㄱ자 구역의 빈 귀퉁이 = 다른 구역은 건드리지 않게)
data modify storage rlk:room q set from entity @s data.cells
data modify storage rlk:room w set from storage rlk:room th
function rlk:room/wave_cells
# 구역 전체를 덮었으면 끝: 한가운데 무늬 표시
execute if score #ax0 tmp = #wx0 tmp if score #ax1 tmp = #wx1 tmp if score #az0 tmp = #wz0 tmp if score #az1 tmp = #wz1 tmp run function rlk:room/wave_end
