# 아이템 조정 묶음 2 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# 모래시계 조각: 개당 재사용 대기 감소를 ‰ 로 (50‰ = 5%, 값은 load 에서 ‰ 로 설정)
# 처형인의 두건: 피해 증가 % (#hoodHp 체력 기준은 고정)
data modify storage rlk:tune t.hood set value [{n:"#hoodDmg",m:"a"}]
data modify storage rlk:tune ids append value "hood"
# 모래시계 조각: 개당 재사용 대기 감소 ‰ (최대 90% 감소 한도는 고정)
data modify storage rlk:tune t.hourglass_shard set value [{n:"#hourglassCd",m:"a"}]
data modify storage rlk:tune ids append value "hourglass_shard"
