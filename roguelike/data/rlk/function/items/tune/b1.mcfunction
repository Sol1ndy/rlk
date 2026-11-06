# 아이템 조정 묶음 1 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# 선장의 팔보호대 · 불사자의 갈기: 받는 피해 감소를 ‰ 로 (60‰ = 6%, 150‰ = 15%, 값은 load 에서 ‰ 로 설정. items/proc/taken 이 ‰ 로 계산)
# 기병대장의 동전: 처치당 원소 에너지 ×100 (100 = 1pt, 공용 #100 대신)
scoreboard players set #cavalryEn tmp 100
# 불사자의 갈기: 반격 화염 피해 = 공격력의 %
scoreboard players set #lionBoomCoef tmp 150
# 선장의 팔보호대: 개당 받는 피해 감소 ‰ (합산 60% 한도는 고정)
data modify storage rlk:tune t.captain_bracer set value [{n:"#bracerRes",m:"a"}]
data modify storage rlk:tune ids append value "captain_bracer"
# 기병대장의 동전: 처치당 원소 에너지
data modify storage rlk:tune t.cavalry_coin set value [{n:"#cavalryEn",m:"a"}]
data modify storage rlk:tune ids append value "cavalry_coin"
# 계약의 잉크: 스킬마다 생명의 계약 (최대 체력의 %, 생명의 계약 상한 #bolMax 는 고정)
data modify storage rlk:tune t.contract_ink set value [{n:"#inkBol",m:"a"}]
data modify storage rlk:tune ids append value "contract_ink"
# 동전 주머니: 처치당 +1 골드는 정수라 그대로 (조정 없음)
# 불사자의 갈기: 받는 피해 감소 ‰ · 반격 피해 계수 · 반격 재사용 대기(틱). 반경 4칸은 고정
data modify storage rlk:tune t.lion_mane set value [{n:"#lionRes",m:"a"},{n:"#lionBoomCoef",m:"a"},{n:"#lionCdT",m:"c"}]
data modify storage rlk:tune ids append value "lion_mane"
