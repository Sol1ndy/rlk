# 땅속으로 (@s = 두뇌): rlk_mob 을 떼고 rlk_pet(몹 준비 대상 아님) → 플레이어 공격 · 자동 조준이 고르지 않음, 체력바 · 클릭 실드도 정리됨. 무적, 다중 처치 대상 아님
tag @s add rlk_c3bur
tag @s add rlk_pet
tag @s remove rlk_mob
data merge entity @s {Invulnerable:1b}
scoreboard players set @s c3B 0
