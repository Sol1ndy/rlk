# 커스텀 몹 피격. @s = 공격한 두뇌/투사체; 플레이어로 실행자를 바꾸기 전에 넉백 방향 저장.
# 입력: #cmDmg 원피해 · #cmEl 원소 · #cmLv 몹 레벨.
kill @e[tag=rlk_plkb_source]
scoreboard players set #cmKB tmp 3
execute if entity @s[tag=rlk_cmp_ar] run scoreboard players set #cmKB tmp 2
execute if entity @s[tag=rlk_cmp_fb] run scoreboard players set #cmKB tmp 2
execute if entity @s[tag=rlk_cmp_cb] run scoreboard players set #cmKB tmp 4
# 얼법은 직격과 바닥 폭발 모두 넉백 제외. 매 피격마다 초기화하여 이전 공격 값이 남지 않는다.
execute if entity @s[tag=rlk_cmic] run scoreboard players set #cmKB tmp 0
execute if entity @s[tag=rlk_cm_im] run scoreboard players set #cmKB tmp 0
execute if score #cmKB tmp matches 1.. run function rlk:cm/knockback_direction
execute as @a[tag=player,limit=1] run function rlk:cm/hit_pl2
kill @e[tag=rlk_plkb_source]
