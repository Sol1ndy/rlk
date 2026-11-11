# @s = 플레이어 (char/motion/dash: 마네킹 캐릭터 — 루미네 · 클로린드 · 로노바 · 네페르 — 의 일반 닷지). 마네킹 아바타가 잠깐 몸을 낮춘다
# (바닐라 웅크림 자세): 리그 캐릭터의 dash 클립과 같은 「웅크리며 내딛는 한 걸음」. 닷지 창이 끝난 다음 틱(누른 지 3틱 뒤)에
# player/def/box_end 가 다시 세운다(player/dodge/stand; #dgCr cb 1 = 세울 것이 있음)
data merge entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] {pose:"crouching"}
scoreboard players set #dgCr cb 1
