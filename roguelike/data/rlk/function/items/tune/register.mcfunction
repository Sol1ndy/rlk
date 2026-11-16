# 아이템 너프 · 강화 배율 (load 에서 items/register 다음에)
# 배율(‰) 표: 강화 단계 0~3 → a 효과량(피해 계수 · % 보너스 · 회복량 · 스택 등) · d 지속 시간 · c 재사용 대기(간격). 0단계 = 너프된 기본, 3단계 = 너프 전 값
data modify storage rlk:tune fac set value [{a:500,d:700,c:1300},{a:667,d:800,c:1200},{a:833,d:900,c:1100},{a:1000,d:1000,c:1000}]
# 아이템별 조정 상수: rlk:tune t.<아이템 id> = [{n:"#상수 이름",m:"a|d|c"}] (상수는 load 에서 '#이름 tmp' 로 매번 설정되는 값)
data modify storage rlk:tune t set value {}
data modify storage rlk:tune ids set value []
function #rlk:tune_tables
# 지금 load 가 넣은 값을 기준값(b)으로 잡고, 아이템마다 강화 단계에 맞춰 상수를 다시 계산 + 설명 숫자 캐시
data modify storage rlk:items disp set value {}
data modify storage rlk:tune iq set from storage rlk:tune ids
function rlk:items/tune/init_loop
