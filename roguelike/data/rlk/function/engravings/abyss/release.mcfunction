# 심연의 원소가 다 모임: 기록한 원소를 발사 대기열로 옮기고 스택을 비운다
scoreboard players operation #aq1 eng += #ab1 eng
scoreboard players operation #aqN eng += #ab1 eng
scoreboard players set #ab1 eng 0
scoreboard players operation #aq2 eng += #ab2 eng
scoreboard players operation #aqN eng += #ab2 eng
scoreboard players set #ab2 eng 0
scoreboard players operation #aq3 eng += #ab3 eng
scoreboard players operation #aqN eng += #ab3 eng
scoreboard players set #ab3 eng 0
scoreboard players operation #aq4 eng += #ab4 eng
scoreboard players operation #aqN eng += #ab4 eng
scoreboard players set #ab4 eng 0
scoreboard players operation #aq5 eng += #ab5 eng
scoreboard players operation #aqN eng += #ab5 eng
scoreboard players set #ab5 eng 0
scoreboard players operation #aq6 eng += #ab6 eng
scoreboard players operation #aqN eng += #ab6 eng
scoreboard players set #ab6 eng 0
scoreboard players operation #aq7 eng += #ab7 eng
scoreboard players operation #aqN eng += #ab7 eng
scoreboard players set #ab7 eng 0
scoreboard players set #abStack eng 0
scoreboard players set #aqT eng 0
execute at @a[tag=player,limit=1] unless score #k211 snd matches 1 run function rlk:snd/f234
execute at @e[tag=rlk_body,limit=1] run particle minecraft:witch ~ ~1.2 ~ 0.4 0.6 0.4 0.2 25
