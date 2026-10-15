# 아이템 조정 묶음 9 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# demonomicon: 마법 발동 간격(틱, 공용 #st20 대신 이 아이템만)
scoreboard players set #demonoInt tmp 20
# sesshou_sakura: 반복 간격(틱, 공용 #st60 대신 이 아이템만)
scoreboard players set #sakInt tmp 60
# 붉은 달의 서약: 생명의 계약 1%당 피해 증가 ‰ (300‰ = 0.3%, 공용 #st3 ÷ #st10 대신. items/proc/moon_bonus 가 ÷1000)
scoreboard players set #cmoonRate tmp 300
# 데모노미콘: 마법 피해 = 공격력의 % (items/proc/demono_dmg 의 고정값 260 대신) · 활성 시간(틱, demono_proc 의 200 대신. 20틱마다 1회라 200 = 10회)
scoreboard players set #demonoCoef tmp 260
scoreboard players set #demonoDur tmp 200
# 장생의 호리병: 회복을 최대 체력의 ‰ 로 (20‰ = 2%, 값은 load 에서 ‰ 로 설정. gourd_heal 이 ‰ 로 계산) · 회복 간격(틱, gourd_tick 의 60 대신)
scoreboard players set #gourdInt tmp 60
# 기계 심장: 낙뢰 피해 = 공격력의 % (items/proc/mech_hit 의 coef 대신)
scoreboard players set #mechCoef tmp 120
# 고통 & 절망: 최대 스택(pd_gain 의 20 대신) · 스택 유지 시간(틱, pd_gain 의 40 대신)
scoreboard players set #pdMax tmp 20
scoreboard players set #pdDur tmp 40
# 살생앵: 그루 수 1 / 2 / 3 일 때 피해 = 공격력의 % (sakura_hit1~3 의 coef 대신)
scoreboard players set #sakCoef1 tmp 35
scoreboard players set #sakCoef2 tmp 50
scoreboard players set #sakCoef3 tmp 65
# 붉은 달의 서약: 1%당 피해 증가 ‰ · 최대 피해 증가 % (같은 배율이라 최대에 닿는 생명의 계약 150% 는 그대로). 원소폭발마다 생명의 계약 30% 는 자원이자 대가라 고정 (#bolMax 도 고정)
data modify storage rlk:tune t.crimson_moon set value [{n:"#cmoonRate",m:"a"},{n:"#cmoonMax",m:"a"}]
data modify storage rlk:tune ids append value "crimson_moon"
# 데모노미콘: 마법 피해 계수 · 활성 시간(틱). 발동 조건 스킬 4회(items/hook/on_skill)는 조건이라 고정, 1초 간격 #st20(demono_tick)은 공용이라 고정 · 사거리 · 반경 고정
data modify storage rlk:tune t.demonomicon set value [{n:"#demonoCoef",m:"a"},{n:"#demonoDur",m:"d"},{n:"#demonoInt",m:"c"}]
data modify storage rlk:tune ids append value "demonomicon"
# 장생의 호리병: 회복 ‰ · 회복 간격(틱) · 체력이 가득일 때 피해 증가 %
data modify storage rlk:tune t.life_gourd set value [{n:"#gourdHeal",m:"a"},{n:"#gourdInt",m:"c"},{n:"#gourdDmg",m:"a"}]
data modify storage rlk:tune ids append value "life_gourd"
# 기계 심장: 낙뢰 피해 계수 · 재사용 대기(틱). 반경 3칸은 고정
data modify storage rlk:tune t.mech_heart set value [{n:"#mechCoef",m:"a"},{n:"#mechCdT",m:"c"}]
data modify storage rlk:tune ids append value "mech_heart"
# 달빛 베틀: 지속 시간(틱) · 원소 마스터리 증가
data modify storage rlk:tune t.moonlit_loom set value [{n:"#loomDur",m:"d"},{n:"#loomEm",m:"a"}]
data modify storage rlk:tune ids append value "moonlit_loom"
# 고통 & 절망: 최대 스택(스택이 금방 차서 최대가 곧 효과량, 단계별 10/13/17/20) · 유지 시간(틱). 스택당 공속 1.5 · 이속 1(pd_apply, 공용 #c3 · #st2)과 1회당 1스택은 고정
data modify storage rlk:tune t.pain_despair set value [{n:"#pdMax",m:"a"},{n:"#pdDur",m:"d"}]
data modify storage rlk:tune ids append value "pain_despair"
# 살생앵: 나무 수명(틱) · 그루 수별 피해 계수. 최대 3그루는 단계 구조라 고정, 3초 간격 #st60(sakura_tick)은 공용이라 고정 · 사거리 10칸 고정
data modify storage rlk:tune t.sesshou_sakura set value [{n:"#sakDur",m:"d"},{n:"#sakCoef1",m:"a"},{n:"#sakCoef2",m:"a"},{n:"#sakCoef3",m:"a"},{n:"#sakInt",m:"c"}]
data modify storage rlk:tune ids append value "sesshou_sakura"
# 음원 샘플: 음원 지속 시간(틱) · 원소 피해 보너스 %. 음원 3개 이상 조건은 고정
data modify storage rlk:tune t.source_samples set value [{n:"#srcDur",m:"d"},{n:"#srcDmg",m:"a"}]
data modify storage rlk:tune ids append value "source_samples"
