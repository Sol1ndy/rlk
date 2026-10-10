# 다음 단계 (@s = 플레이어). 마지막 단계에서 누르면 처음부터
scoreboard players set #tutW lob 0
scoreboard players add #tutS lob 1
execute if score #tutS lob matches 12..20 run scoreboard players set #tutS lob 1
# 캐릭터 튜토리얼: 추가 설명(5쪽)이 없는 캐릭터는 건너뜀, 끝에서 누르면 처음부터
execute if score #tutS lob matches 24 unless data storage rlk:chars cur.info.passive[0] run scoreboard players set #tutS lob 25
execute if score #tutS lob matches 25 unless data storage rlk:chars cur.info.extra.lore[0] run scoreboard players set #tutS lob 26
execute if score #tutS lob matches 27.. run scoreboard players set #tutS lob 21
function rlk:lobby/tut/stage
