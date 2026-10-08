# 피격 숫자 표시 (입력: #hurtDmg, #elem). 물리 = 빨강, 원소 = 원소 색
execute store result storage rlk:combat hd int 1 run scoreboard players get #hurtDmg tmp
function rlk:element/color
execute unless score #elem tmp matches 1.. run data modify storage rlk:combat col set value "red"
function rlk:player/hurt_text_macro with storage rlk:combat
