# @s = 플레이어. 가드 자세(받은 F): 리그 캐릭터(아를레키노 · 스커크 · 나비아)는 가드 클립(char/motion/guard), 아바타 마네킹
# 캐릭터(루미네 · 클로린드 · 로노바 · 네페르)는 왼손을 휘둘러 막는 몸짓. 칼끝 앞에 작은 금빛 반짝임
function rlk:char/motion/guard
execute unless score #charN tmp matches 3 unless score #charN tmp matches 5..6 as @e[tag=rlk_av,limit=1] run swing @s offhand
# round W(검토 T3-01: 원작은 접점 0.35~0.2초 전에 칼을 드는 바람 소리가 있다): 가드를 드는 짧은 바람
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.sweep player @a[tag=player] ~ ~ ~ 0.35 1.6
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^1.2 ^0.6 run particle minecraft:dust{color:[1.0f,0.86f,0.45f],scale:0.7f} ~ ~ ~ 0.15 0.2 0.15 0 4 normal @a[tag=player]
