scoreboard players set @s skillCd 0
scoreboard players set @s burstCd 0
# 원소 에너지: 필요량보다 크게 넣으면 char/tick 이 필요량으로 맞춘다(스커크는 뱀의 계략 최대치)
scoreboard players set @s energy 9999999
# 캐릭터별 충전 · 간격
scoreboard players set @s nvC 2
scoreboard players set @s nvCT 0
scoreboard players set @s nvFcd 0
scoreboard players set @s rnFcd 0
scoreboard players set @s clLCd 0
scoreboard players set @s skDepCd 0
tellraw @s [{"text":"[테스트] ","color":"gold"},{"text":"스킬 · 폭발 재사용 대기와 원소 에너지를 채웠습니다.","color":"gray"}]
