# 스코어보드 값 -> 바닐라 속성 반영 (@s = 플레이어)
# 이동 속도: base 0.1 * (moveSpeed / 100)
execute store result storage rlk:calc ms double 0.001 run scoreboard players get @s moveSpeed
# 공격 속도: base 4.0 * (atkSpeed / 100)
execute store result storage rlk:calc as double 0.04 run scoreboard players get @s atkSpeed
function rlk:player/apply_attributes_macro with storage rlk:calc
