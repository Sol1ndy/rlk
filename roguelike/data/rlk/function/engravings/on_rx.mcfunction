# 원소 반응이 일어남 (@s = 맞은 몹 또는 풀 씨앗, #rx = 반응 번호, #elem = 닿은 원소). element/on_hit · core_hyper · core_burgeon 에서 호출
# 캐릭터: 스커크의 허계 균열
execute if score #charN tmp matches 3 run function rlk:char/skirk/on_rx
# 아이템: 반응이 일어났을 때
function rlk:items/hook/on_rx
# 침식 5개: 반응이 일어난 적에게 표시
execute if score erode engN matches 5.. if entity @s[tag=rlk_mob] run function rlk:engravings/erode/mark
# 증폭 4개: 증발(1)·융해(2) 로 주는 피해 +#ampRx%
execute if score amplify engN matches 4.. if score #rx tmp matches 1..2 unless score #tfm tmp matches 1 run function rlk:engravings/amp_rx
# 뇌명: 과부하(3)·초전도(4)·감전(5) 피해 증가 / 스킬 재사용 대기 감소
execute if score thunder engN matches 2.. if score #rx tmp matches 3..5 run function rlk:engravings/thunder/rx
# 원소 4개: 심연의 원소 +1, 반응에 쓰인 두 원소 기록 (심연의 탄환이 일으킨 반응은 세지 않음)
execute unless score elemental engN matches 4.. run return 0
execute if score #abyssHit tmp matches 1 run return 0
execute if score #rx tmp matches 1 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 1 run scoreboard players add #ab2 eng 1
execute if score #rx tmp matches 2 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 2 run scoreboard players add #ab4 eng 1
execute if score #rx tmp matches 3 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 3 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 4 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 4 run scoreboard players add #ab4 eng 1
execute if score #rx tmp matches 5 run scoreboard players add #ab2 eng 1
execute if score #rx tmp matches 5 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 6 run scoreboard players add #ab2 eng 1
execute if score #rx tmp matches 6 run scoreboard players add #ab4 eng 1
execute if score #rx tmp matches 10 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 10 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 11 run scoreboard players add #ab2 eng 1
execute if score #rx tmp matches 11 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 12 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 12 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 13 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 13 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 14 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 14 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 15 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 15 run scoreboard players add #ab7 eng 1
execute if score #rx tmp matches 16 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 16 run scoreboard players add #ab7 eng 1
# 쇄빙(7): 얼음 + (바위로 깼으면 바위)
execute if score #rx tmp matches 7 run scoreboard players add #ab4 eng 1
execute if score #rx tmp matches 7 if score #elem tmp matches 5 run scoreboard players add #ab5 eng 1
# 확산(8) = 바람 + 퍼진 원소, 결정(9) = 바위 + 닿은 원소 (그 원소 번호는 몹의 rxEl)
execute if score #rx tmp matches 8 run scoreboard players add #ab6 eng 1
execute if score #rx tmp matches 9 run scoreboard players add #ab5 eng 1
execute if score #rx tmp matches 8..9 if score @s rxEl matches 1 run scoreboard players add #ab1 eng 1
execute if score #rx tmp matches 8..9 if score @s rxEl matches 2 run scoreboard players add #ab2 eng 1
execute if score #rx tmp matches 8..9 if score @s rxEl matches 3 run scoreboard players add #ab3 eng 1
execute if score #rx tmp matches 8..9 if score @s rxEl matches 4 run scoreboard players add #ab4 eng 1
scoreboard players add #abStack eng 1
execute at @a[tag=player,limit=1] unless score #k209 snd matches 1 run function rlk:snd/f232
execute if score #abStack eng >= #abyssMax tmp run function rlk:engravings/abyss/release
