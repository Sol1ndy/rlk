# @s = 플레이어 (char/motion/dash · dash_l · dash_b: 마네킹 캐릭터 — 루미네 · 클로린드 · 로노바 · 네페르 — 의 닷지 동작). 마네킹 아바타가
# 몸을 낮춘다(바닐라 마네킹 자세 crouching): 리그 캐릭터의 비틀기 · 걸음 · 백스텝 클립 대신. 닷지 이동이 끝나는 틱에
# player/dash_move_tick 이 다시 세운다(player/dodge/stand; #dgCr cb 1 = 세울 것이 있음)
data merge entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] {pose:"crouching"}
scoreboard players set #dgCr cb 1
