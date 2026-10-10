# 지금 단계(#tutS) 준비 (@s = 플레이어)
kill @e[tag=rlk_tutE]
# 앞 단계에서 남은 캐릭터 소환물(루미네의 혹한의 별 등)이 다음 단계 목표를 대신 채우지 않게
function rlk:run/field_clear
scoreboard players set #tutC lob 0
scoreboard players set #tutCp lob -1
scoreboard players set #tutW lob 0
execute if score #tutS lob matches 1 run function rlk:lobby/tut/s1
execute if score #tutS lob matches 2 run function rlk:lobby/tut/s2
execute if score #tutS lob matches 3 run function rlk:lobby/tut/s3
execute if score #tutS lob matches 4 run function rlk:lobby/tut/s4
execute if score #tutS lob matches 5 run function rlk:lobby/tut/s5
execute if score #tutS lob matches 6 run function rlk:lobby/tut/s6
execute if score #tutS lob matches 7 run function rlk:lobby/tut/s7
execute if score #tutS lob matches 8 run function rlk:lobby/tut/s8
execute if score #tutS lob matches 9 run function rlk:lobby/tut/s9
execute if score #tutS lob matches 10 run function rlk:lobby/tut/s10
execute if score #tutS lob matches 11 run function rlk:lobby/tut/s11
execute if score #tutS lob matches 21.. run function rlk:lobby/ct/page
function rlk:lobby/tut/goal
execute unless score #k74 snd matches 1 run function rlk:snd/f79
