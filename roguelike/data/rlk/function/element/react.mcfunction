# 원소 #elem(#elU) 이 @s 에 닿음 → 붙어 있는 원소와 반응하거나 부착 (@s = 몹 또는 플레이어, at @s)
# 출력: #rx(반응 번호, 0=없음), #mulPct(증폭 배율%), #addDmg(추가 피해). 격변 반응은 @s 의 rxQ/rxDmg/rxEl 에 예약
# 공허 반응: 17 소각 18 심연 19 단죄 20 빙참 21 공허 결정 22 진공 23 공허 개화 (= 16 + 닿은/붙어 있던 다른 원소 번호)
# 반응 번호: 1 증발 2 융해 3 과부하 4 초전도 5 감전 6 빙결 7 쇄빙 8 확산 9 결정 10 연소 11 개화 12 만개 13 발화 14 활성 15 촉진 16 발산
scoreboard players set #rx tmp 0
scoreboard players set #lunRx tmp 0
scoreboard players set #mulPct tmp 100
scoreboard players set #addDmg tmp 0
execute if score #elem tmp matches 1 run function rlk:element/on/fire
execute if score #elem tmp matches 2 run function rlk:element/on/water
execute if score #elem tmp matches 3 run function rlk:element/on/thunder
execute if score #elem tmp matches 4 run function rlk:element/on/ice
execute if score #elem tmp matches 5 run function rlk:element/on/rock
execute if score #elem tmp matches 6 run function rlk:element/on/wind
execute if score #elem tmp matches 7 run function rlk:element/on/grass
execute if score #elem tmp matches 8 run function rlk:element/on/void
# 증폭 반응(증발·융해): 원소 마스터리 보정
execute if score #mulPct tmp matches 101.. run function rlk:element/amp_em
