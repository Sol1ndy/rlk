# 시험용: /function rlk:cm/test {t:"sw"}  (1챕터: sw 검사 · ar 궁수 · fm 불 마법사 · im 얼음 마법사 · sh 방패병 · cn 대포병 / 2챕터: ns 떠돌이 무사 졸개 · sl 번개 슬라임 · ss 작은 번개 슬라임 · sp 반란군 창병 · dr 오니 북잡이 · kr 카이라기·뇌전 · nj 그림자 닌자 · cc 번개 시킨 술사 · ci 번개 시킨 / 무리: g_ns 졸개 4~6 · g_sp 창병 대열 3 · g_sl 슬라임 2~3) — 바라보는 쪽 5칸 앞에 1레벨로
# 숄더뷰에서는 카메라 대신 몸의 발 위치를 사용하고, 방향은 명령을 실행한 플레이어의 시선을 따른다.
$execute if entity @s[tag=player] if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
$execute unless entity @s[tag=player] at @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
$execute if entity @s[tag=player] unless entity @e[tag=rlk_body,limit=1] at @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
execute as @e[tag=rlk_newmob] run function rlk:cm/test_init
