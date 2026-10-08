# @s = 방금 언 몹: 얼음(탑승 엔티티)의 실제 높이를 읽어 얼음 바닥이 발밑 5cm 아래에 오도록 보정
# 탑승 직후에는 얼음 위치가 아직 몹 발밑으로 나오므로, 위치가 갱신된 틱에 적용한다
execute store result score #fy0 tmp run data get entity @s Pos[1] 1000
scoreboard players operation #fy1 tmp = #fy0 tmp
execute on passengers if entity @s[tag=rlk_frz_ice] store result score #fy1 tmp run data get entity @s Pos[1] 1000
scoreboard players operation #fy0 tmp -= #fy1 tmp
scoreboard players remove #fy0 tmp 50
execute if score #fy0 tmp matches ..-100 on passengers if entity @s[tag=rlk_frz_ice] store result entity @s transformation.translation[1] float 0.001 run scoreboard players get #fy0 tmp
execute if score #fy0 tmp matches ..-100 run tag @s remove rlk_frz_fix
