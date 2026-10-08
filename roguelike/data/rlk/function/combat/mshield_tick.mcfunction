# 몹 클릭 실드: 고아 정리 + 클릭 폴링 (몹 처리 이후 호출됨)
# 이번 틱에 주인 몹이 동기화 안 한 실드 = 몹 사망/소멸 → 제거
kill @e[tag=rlk_mshield,tag=!rlk_msync]
tag @e[tag=rlk_mshield] remove rlk_msync
# 좌클릭 → 공격 경로(on_attack), 우클릭 → 대쉬/스킬 경로(rclick_do)
execute as @e[tag=rlk_mshield] if data entity @s attack at @s run function rlk:combat/mshield_click
execute as @e[tag=rlk_mshield] if data entity @s interaction at @s run function rlk:combat/mshield_rclick
