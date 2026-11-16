# @s = 박자가 세워 둔 몹. 세우기 전에는 NoAI 가 아니었다: 멈춘 동안 시작된 빙결 · 그로기가 "원래 NoAI" 로 기억한 표식(rlk_noai ·
# rlk_bal_noai)은 틀린 것이라 지우고, 빙결 · 그로기가 걸려 있지 않으면 여기서 AI 를 돌려준다(걸려 있으면 그쪽이 끝날 때 돌려준다)
tag @s remove rlk_bt_noai
tag @s remove rlk_noai
tag @s remove rlk_bal_noai
execute unless score @s frzT matches 1.. unless score @s grgT matches 1.. run data merge entity @s {NoAI:0b}
