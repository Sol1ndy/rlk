# 아이템 조정 묶음 4 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# 격려의 깃발 · 지니 램프 · 정화의 풀고리: 회복량을 최대 체력의 ‰ 로 (20‰ = 2%, 값은 load 에서 ‰ 로 설정. flag_heal · genie_pulse · gring_pulse 가 ‰ 로 계산)
# 불꽃 방벽: 적중당 보호막을 최대 체력의 ‰ 로 (20‰ = 2%, 값은 load 에서 ‰ 로 설정. barrier 가 ‰ 로 계산. 한도 #barCap 은 % 그대로)
# 토끼 백작: 폭발 피해 = 공격력의 % · 인형 체력
scoreboard players set #bunnyBoomCoef tmp 100
scoreboard players set #bunnyHp tmp 80
# 퇴마의 부적: 얼음 원소 부여 지속 시간(틱)
scoreboard players set #exoDur tmp 160
# 정화의 풀고리: 번개 피해 = 공격력의 %
scoreboard players set #gringCoef tmp 25
# 격려의 깃발: 깃발 수명(틱) · 공격력 증가 % · 회복 ‰ (1초 간격 #st20 · 반경 4칸은 고정)
data modify storage rlk:tune t.banner set value [{n:"#flagDur",m:"d"},{n:"#flagAtk",m:"a"},{n:"#flagHeal",m:"a"}]
data modify storage rlk:tune ids append value "banner"
# 토끼 백작: 인형 수명(틱) · 폭발 피해 계수 · 인형 체력 · 재사용 대기(틱). 도발 반경 10칸 · 폭발 반경 4칸은 고정
data modify storage rlk:tune t.baron_bunny set value [{n:"#bunnyDur",m:"d"},{n:"#bunnyBoomCoef",m:"a"},{n:"#bunnyHp",m:"a"},{n:"#bunnyCdT",m:"c"}]
data modify storage rlk:tune ids append value "baron_bunny"
# 불꽃 방벽: 적중당 보호막 ‰ · 보호막 한도 % (같은 배율이라 채우는 적중 수는 그대로) · 재사용 대기(틱). 보호막 15초 유지는 공용 규칙이라 고정
data modify storage rlk:tune t.blazing_barrier set value [{n:"#barAdd",m:"a"},{n:"#barCap",m:"a"},{n:"#barCdT",m:"c"}]
data modify storage rlk:tune ids append value "blazing_barrier"
# 고양이 꼬리 칵테일: 이동 속도 · 공격 속도 증가 % (한 상수)
data modify storage rlk:tune t.cat_cocktail set value [{n:"#cocktailSpd",m:"a"}]
data modify storage rlk:tune ids append value "cat_cocktail"
# 퇴마의 부적: 얼음 원소 부여 지속 시간(틱)
data modify storage rlk:tune t.exorcist_charm set value [{n:"#exoDur",m:"d"}]
data modify storage rlk:tune ids append value "exorcist_charm"
# 페보니우스 비전: 원소 에너지(×100) · 재사용 대기(틱). 발동 확률 #favChance 60% 는 고정 (에너지와 같이 줄이면 겹쳐서 너프)
data modify storage rlk:tune t.favonius_codex set value [{n:"#favEnergy",m:"a"},{n:"#favCdT",m:"c"}]
data modify storage rlk:tune ids append value "favonius_codex"
# 대장의 군기: 군기 수명(틱) · 방어력 증가 % · 바위 원소 피해 보너스 % (반경 4칸은 고정)
data modify storage rlk:tune t.general_banner set value [{n:"#gflagDur",m:"d"},{n:"#gflagDef",m:"a"},{n:"#gflagDmg",m:"a"}]
data modify storage rlk:tune ids append value "general_banner"
# 지니 램프: 지속 시간(틱) · 원소 에너지(×100) · 회복 ‰ (2초 간격 #st40 은 공용이라 고정)
data modify storage rlk:tune t.genie_lamp set value [{n:"#genieDur",m:"d"},{n:"#genieEnergy",m:"a"},{n:"#genieHeal",m:"a"}]
data modify storage rlk:tune ids append value "genie_lamp"
# 정화의 풀고리: 지속 시간(틱) · 번개 피해 계수 · 회복 ‰ (체력 소모 #gringCost 20% 는 대가라 고정, 1.5초 간격 #st30 · 반경 3.5칸도 고정)
data modify storage rlk:tune t.grass_ring set value [{n:"#gringDur",m:"d"},{n:"#gringCoef",m:"a"},{n:"#gringHeal",m:"a"}]
data modify storage rlk:tune ids append value "grass_ring"
# 성스러운 방패: 기본 공격 피해 증가 % · 지속 시간(틱)
data modify storage rlk:tune t.holy_shield set value [{n:"#candDmg",m:"a"},{n:"#candDur",m:"d"}]
data modify storage rlk:tune ids append value "holy_shield"
