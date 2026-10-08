# 달리기 시작/끝 (@s = 플레이어): 시야 넓힘 수정자 붙이기/떼기. 넓어지는 정도 = 아래 숫자(0.1 = 이동 속도 +10% → 시야 약 +5%. 0 에 가까울수록 덜 넓어짐)
scoreboard players operation #spr view = #sprNow view
execute if score #spr view matches 1 run attribute @s minecraft:movement_speed modifier add rlk:view_sprint 0.1 add_multiplied_total
execute if score #spr view matches 0 run attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
