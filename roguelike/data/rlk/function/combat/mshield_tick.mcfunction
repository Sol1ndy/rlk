# 몹이 같은 틱에 죽거나 뷰 전환으로 실드가 고아가 되어도, 남아 있는 클릭부터 소비한다.
execute as @e[tag=rlk_mshield] if data entity @s attack at @s run function rlk:combat/mshield_click
execute as @e[tag=rlk_mshield] if data entity @s interaction at @s run function rlk:combat/mshield_rclick
# 클릭 처리 뒤 고아를 정리한다.
kill @e[tag=rlk_mshield,tag=!rlk_msync]
tag @e[tag=rlk_mshield] remove rlk_msync
