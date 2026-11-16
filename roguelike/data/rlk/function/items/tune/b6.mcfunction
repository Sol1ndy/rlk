# 아이템 조정 묶음 6 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# raven_feather: 반복 간격(틱, 공용 #st20 대신 이 아이템만)
scoreboard players set #ravenItv tmp 20
# 서약의 단검: 원소폭발마다 생명의 계약 = 최대 체력의 % (dagger_bol 의 숫자 20 대신)
scoreboard players set #daggerBol tmp 20
# 빗줄기 검집 · 밤까마귀의 깃 · 텐구의 깃: 피해 = 공격력의 % (rain_sword · raven_hit · tengu_boom 의 coef 대신)
scoreboard players set #rainCoef tmp 25
scoreboard players set #ravenCoef tmp 30
scoreboard players set #tenguCoef tmp 60
# 비운 깃발: 지속 시간(틱) · 강화 적중 횟수 · 더해지는 피해 방어력의 ‰
data modify storage rlk:tune t.opera_flag set value [{n:"#operaDur",m:"d"},{n:"#operaMax",m:"a"},{n:"#operaPm",m:"a"}]
data modify storage rlk:tune ids append value "opera_flag"
# 서약의 단검: 공격 속도 증가 % · 생명의 계약 % (생명의 계약 상한 #bolMax 는 고정)
data modify storage rlk:tune t.pact_dagger set value [{n:"#daggerSpd",m:"a"},{n:"#daggerBol",m:"a"}]
data modify storage rlk:tune ids append value "pact_dagger"
# 빗줄기 검집: 지속 시간(틱) · 피해 계수 · 재사용 대기(틱). 사거리 7칸은 고정
data modify storage rlk:tune t.rain_sheath set value [{n:"#rainDur",m:"d"},{n:"#rainCoef",m:"a"},{n:"#rainCdT",m:"c"}]
data modify storage rlk:tune ids append value "rain_sheath"
# 밤까마귀의 깃: 지속 시간(틱) · 피해 계수. 1초 간격 #st20 은 공용이라 고정 (raven_tick 이 이 묶음 밖), 사거리 12칸도 고정
data modify storage rlk:tune t.raven_feather set value [{n:"#ravenDur",m:"d"},{n:"#ravenCoef",m:"a"},{n:"#ravenItv",m:"c"}]
data modify storage rlk:tune ids append value "raven_feather"
# 죄인의 창끝: 지속 시간(틱) · 치명타 확률 증가 %
data modify storage rlk:tune t.sinner_spear set value [{n:"#sinDur",m:"d"},{n:"#sinCrit",m:"a"}]
data modify storage rlk:tune ids append value "sinner_spear"
# 텐구의 깃: 공격력 증가 지속(틱) · 공격력 증가 % · 피해 계수. 번개까지 1.5초(tengu_place 의 life 30) · 반경 3.5칸은 고정
data modify storage rlk:tune t.tengu_feather set value [{n:"#tenguDur",m:"d"},{n:"#tenguAtk",m:"a"},{n:"#tenguCoef",m:"a"}]
data modify storage rlk:tune ids append value "tengu_feather"
# 도둑의 장갑: 재사용 대기(틱)만. 골드 #thiefGold 1 은 정수라 그대로 (줄이면 0 이 되어 효과가 사라짐)
data modify storage rlk:tune t.thief_gloves set value [{n:"#thiefCdT",m:"c"}]
data modify storage rlk:tune ids append value "thief_gloves"
# 바람 슬라임 인형: 지속 시간(틱) · 원소 마스터리 증가
data modify storage rlk:tune t.wind_slime set value [{n:"#slimeDur",m:"d"},{n:"#slimeEm",m:"a"}]
data modify storage rlk:tune ids append value "wind_slime"
