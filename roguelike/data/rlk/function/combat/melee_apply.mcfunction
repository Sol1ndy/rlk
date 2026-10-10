# 기존 사거리로 골라진 근접 평타 후보만 처리. @s = 몹, at @s.
function rlk:combat/melee_front
execute if score #meleeFront tmp matches 1 run function rlk:combat/apply_reset
