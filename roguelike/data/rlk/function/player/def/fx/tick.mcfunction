# @s = 효과 엔티티, at @s. cb = 남은 틱. 효과는 만들어진 틱에도 한 번 나이를 먹으므로(rlk:tick 의 fx/world 는 그 틱의 피격들 뒤),
# 만드는 쪽이 한 틱 더한 값으로 시작한다(별빛 6 · 작은 불꽃 4 · 터짐 4 · 번개 3 · 잔상 9 · 경고 섬광 6)
scoreboard players remove @s cb 1
# 붉은 잔상(마네킹)은 kill 하면 클라이언트가 20틱의 사망 동작(쓰러짐)과 연기를 보여 준다: 끝나기 한 틱 전에 보이지 않게 치운 뒤
# (fx/ghost_out) 다음 틱에 거기서 지운다
execute if entity @s[tag=rlk_cb_ghost] if score @s cb matches 1 run return run function rlk:player/def/fx/ghost_out
execute if score @s cb matches ..0 run return run kill @s
execute if entity @s[tag=rlk_cb_star] run return run function rlk:player/def/fx/t_star
execute if entity @s[tag=rlk_cb_glint] run return run function rlk:player/def/fx/t_glint
execute if entity @s[tag=rlk_cb_spark] run return run function rlk:player/def/fx/t_spark
execute if entity @s[tag=rlk_cb_burst] run return run function rlk:player/def/fx/t_burst
