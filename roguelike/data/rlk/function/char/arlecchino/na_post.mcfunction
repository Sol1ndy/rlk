# 일반 공격 뒤 (@s = 플레이어, at 몸)
# 적중(누구든 한 명만 맞혀도): 모든 적의 핏값을 회수
execute if score #hitLanded tmp matches 1 run function rlk:char/arlecchino/absorb_all
# 가면 중 적중: 생명의 계약 소모 + 스킬 재사용 대기 감소
execute if score #arUsed tmp matches 1 if score #hitLanded tmp matches 1 run function rlk:char/arlecchino/mask_use
scoreboard players set #arUsed tmp 0
