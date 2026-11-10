# 피해 문맥 (@s = 바닐라 피해를 준 엔티티(on attacker: 투사체면 쏜 것); view/av_tick · element/on_player_hurt). 등급: boss · miniboss
# 태그면 보스(2), 정예 표시면 1, 그 밖 0. 종류 1(근접, 바닐라는 구분하지 않음). 패링 · 닷지 모두 됨
tag @s add rlk_hc_atk
scoreboard players set #hcK tmp 1
execute if entity @s[tag=rlk_c2e] run scoreboard players set #hcC tmp 1
execute if entity @s[tag=rlk_c3e] run scoreboard players set #hcC tmp 1
execute if entity @s[tag=miniboss] run scoreboard players set #hcC tmp 2
execute if entity @s[tag=boss] run scoreboard players set #hcC tmp 2
