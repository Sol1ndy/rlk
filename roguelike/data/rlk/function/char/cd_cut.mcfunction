# @s = 플레이어. 원소전투 스킬의 재사용 대기를 #cut cb 틱 줄인다(모든 캐릭터; 퍼펙트 패링 −1초 = player/def/par3_go).
# 나비아 · 네페르는 skillCd 를 충전 타이머가 매 틱 다시 쓰므로 그 타이머(nvCT / nfCT, 충전이 2 미만일 때)를 앞당긴다:
# 다음 캐릭터 틱(navia/tick · nefer/tick)이 충전을 채우고 스킬 칸의 남은 시간을 다시 쓴다. 그 밖의 캐릭터는 skillCd(최소 0)
execute if score #charN tmp matches 6 if score @s nvC matches ..1 run return run scoreboard players operation @s nvCT += #cut cb
execute if score #charN tmp matches 8 if score @s nfC matches ..1 run return run scoreboard players operation @s nfCT += #cut cb
execute unless score @s skillCd matches 1.. run return 0
scoreboard players operation @s skillCd -= #cut cb
execute if score @s skillCd matches ..-1 run scoreboard players set @s skillCd 0
