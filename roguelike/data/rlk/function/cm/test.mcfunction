# 시험용: /function rlk:cm/test {t:"sw"} — 바라보는 쪽 5칸 앞에 1레벨로. 쓸 수 있는 id: {t:"help"} (cm/test_help: tools/help_lib.py 의 1챕터 목록 + 챕터마다 몹 생성기가 쓰는 cm/c<N>/test_help)
# 숄더뷰에서는 카메라 대신 몸의 발 위치를 사용하고, 방향은 명령을 실행한 플레이어의 시선을 따른다.
$data modify storage rlk:tmp hq set value "$(t)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:cm/test_help
$execute if entity @s[tag=player] if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
$execute unless entity @s[tag=player] at @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
$execute if entity @s[tag=player] unless entity @e[tag=rlk_body,limit=1] at @s rotated ~ 0 positioned ^ ^ ^5 run function rlk:cm/spawn/$(t)
execute as @e[tag=rlk_newmob] run function rlk:cm/test_init
