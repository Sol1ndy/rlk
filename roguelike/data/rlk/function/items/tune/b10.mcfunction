# 아이템 조정 묶음 10 (items/tune/register 가 function tag #rlk:tune_tables 로 부름: 이 묶음 아이템의 새 상수 + 조정 표 rlk:tune t.<id>)
# skyward_verse: 반복 간격(틱, 공용 #st8 대신 이 아이템만)
scoreboard players set #stormInt tmp 8
# salon_invite: 반복 간격(틱, 공용 #st30 대신 이 아이템만)
scoreboard players set #salonInt tmp 30
# moon_chalice: 반복 간격(틱, 공용 #st40 대신 이 아이템만)
scoreboard players set #cgRipInt tmp 40
# ember_oath: 반복 간격(틱, 공용 #st40 대신 이 아이템만)
scoreboard players set #ringInt tmp 40
# 마검 키리온: 평타 참격 피해 = 공격력의 % (kirion_dmg_calc 의 고정값 60 대신. 대쉬 참격은 이 값 ÷ 2)
scoreboard players set #kirionCoef tmp 60
# 수련의 무희: 물 범위 피해 = 최대 체력의 ‰ (lily_boom 의 pm 대신)
scoreboard players set #lilyPm tmp 40
# 불씨의 맹약: 불볕의 고리 피해 = 공격력의 % (ring_hit 의 coef 대신)
scoreboard players set #ringCoef tmp 50
# 옥장 방패: 운석 피해 = 공격력의 % + 최대 체력의 % (meteor_calc 의 coef · 공용 #st20 대신)
scoreboard players set #meteorCoef tmp 400
scoreboard players set #meteorHp tmp 20
# 서리달의 은잔: 종류별 중력 재사용 대기(틱, cg_gain 의 20 대신)
scoreboard players set #cgTypeCd tmp 20
# 살롱의 초대장: 멤버 공격 피해 = 최대 체력의 ‰ (salon_hit 의 pm 대신)
scoreboard players set #salonPm tmp 60
# 스칸다의 씨앗: 폭발 피해 = 공격력의 % (skandha_calc 의 coef 대신) + 원소 마스터리의 ‰ (공용 #st10 나눗셈 대신 100‰ = 10%)
scoreboard players set #skCoef tmp 80
scoreboard players set #skEm tmp 100
# 바람 신의 시: 폭풍의 눈 · 띄워 올리기 피해 = 공격력의 % (storm_hit · updraft 의 coef 대신)
scoreboard players set #stormCoef tmp 40
scoreboard players set #updraftCoef tmp 150
# 초월 · 악요개안: 협동 공격 피해 = 공격력의 % (eye_strike 의 coef 대신) · 재사용 대기(틱, eye_queue 의 20 대신) · 원소 에너지 1pt당 폭발 피해 증가 0.01% 단위 (30 = 0.3%, 공용 #st3 대신. eye_burst 가 ÷10 해서 ‰)
scoreboard players set #eyeCoef tmp 71
scoreboard players set #eyeCdT tmp 20
scoreboard players set #eyeRate tmp 30
# 마검 키리온: 참격 피해 계수 (대쉬 참격은 ÷2 라 같이 바뀜). 반경 3.5 · 3칸, 대쉬 참격 지연 6틱 · 마커 2틱 간격은 고정
data modify storage rlk:tune t.sword_kirion set value [{n:"#kirionCoef",m:"a"}]
data modify storage rlk:tune ids append value "sword_kirion"
# 수련의 무희: 피해 ‰ · 스킬 뒤 유효 시간(틱) · 재사용 대기(틱). 반경 4칸은 고정
data modify storage rlk:tune t.water_lily set value [{n:"#lilyPm",m:"a"},{n:"#lilyDur",m:"d"},{n:"#lilyCdT",m:"c"}]
data modify storage rlk:tune ids append value "water_lily"
# 불씨의 맹약: 고리 지속 시간(틱) · 고리 피해 계수 · 최대 전의(전의가 금방 차서 최대가 곧 효과량, 단계별 25/33/42/50) · 기본 공격 증가 지속(틱)
# 전의 1당 폭발 +2% · 기본 공격 +1% 는 고정 (#oathMax 와 같이 줄이면 겹쳐서 너프, 2 는 너무 거침). 2초 간격 #st40(ring_tick)은 공용이라 고정 · 반경 3.5칸 고정
data modify storage rlk:tune t.ember_oath set value [{n:"#ringDur",m:"d"},{n:"#ringCoef",m:"a"},{n:"#oathMax",m:"a"},{n:"#oathDur",m:"d"},{n:"#ringInt",m:"c"}]
data modify storage rlk:tune ids append value "ember_oath"
# 옥장 방패: 보호막 % · 보호막 · 취약 지속 시간(틱) · 받는 피해 증가 % · 운석 피해 계수 · 운석 최대 체력 %. 취약 범위 8칸 · 운석 거리 6칸 · 낙하 1초 · 반경 6칸은 고정
data modify storage rlk:tune t.jade_shard set value [{n:"#jadePct",m:"a"},{n:"#jadeDur",m:"d"},{n:"#jadeRes",m:"a"},{n:"#meteorCoef",m:"a"},{n:"#meteorHp",m:"a"}]
data modify storage rlk:tune ids append value "jade_shard"
# 서리달의 은잔: 물결 지속 시간(틱) · 물결 피해 ‰ · 종류별 중력 재사용 대기(틱, 발동 빈도는 이것만으로 c 배율) · 중력 간섭 피해 % · 월광 지속 시간(틱) · 월광 달 반응 피해 %
# 발동 중력 #cgMax 60 · 반응 1번당 #cgGain 20 은 고정 (#cgMax 를 바꾸면 반응 수가 정수라 0~2단계가 모두 4번으로 같아짐, #cgGain 을 바꾸면 #cgTypeCd 와 겹쳐 너프). 2초 간격 #st40(cg_rip_tick)은 공용이라 고정 · 반경 4 · 6칸 고정
data modify storage rlk:tune t.moon_chalice set value [{n:"#cgRipDur",m:"d"},{n:"#cgRipPm",m:"a"},{n:"#cgTypeCd",m:"c"},{n:"#cgGI",m:"a"},{n:"#cgMoonDur",m:"d"},{n:"#cgMoon",m:"a"},{n:"#cgRipInt",m:"c"}]
data modify storage rlk:tune ids append value "moon_chalice"
# 살롱의 초대장: 멤버 지속 시간(틱) · 멤버 피해 ‰ · 체력을 낸 공격 피해 증가 % · 열기 지속 시간(틱) · 열기 획득량 · 열기 최대치(획득량과 같은 배율이라 피해 증가가 그대로 배율만큼 줄어듦)
# 체력 소모 #salonCost 2% 는 대가라 고정, 열기 1당 0.3%(fan_bonus 의 공용 #st3 ÷ #st10)는 고정. 1.5초 간격 #st30(salon_tick)은 공용이라 고정 · 사거리 12칸 고정
data modify storage rlk:tune t.salon_invite set value [{n:"#salonDur",m:"d"},{n:"#salonPm",m:"a"},{n:"#salonDmg",m:"a"},{n:"#fanDur",m:"d"},{n:"#fanGain",m:"a"},{n:"#fanMax",m:"a"},{n:"#salonInt",m:"c"}]
data modify storage rlk:tune ids append value "salon_invite"
# 스칸다의 씨앗: 씨앗 지속 시간(틱) · 폭발 피해 계수 · 원소 마스터리 ‰ · 재사용 대기(틱) · 원소 마스터리 증가 · 증가 지속 시간(틱). 사거리 20칸 고정
data modify storage rlk:tune t.skandha_seed set value [{n:"#skDur",m:"d"},{n:"#skCoef",m:"a"},{n:"#skEm",m:"a"},{n:"#skCdT",m:"c"},{n:"#mayaEm",m:"a"},{n:"#mayaDur",m:"d"}]
data modify storage rlk:tune ids append value "skandha_seed"
# 바람 신의 시: 폭풍의 눈 수명(틱, 0.4초마다 1회라 타격 수도 같이 줄어듦) · 폭풍 피해 계수 · 돌려받는 원소 에너지(×100) · 띄워 올리기 피해 계수. 0.4초 간격 #st8(storm_tick)은 공용이라 고정 · 끌어당기기 · 반경 고정
data modify storage rlk:tune t.skyward_verse set value [{n:"#stormDur",m:"d"},{n:"#stormCoef",m:"a"},{n:"#stormEnergy",m:"a"},{n:"#updraftCoef",m:"a"},{n:"#stormInt",m:"c"}]
data modify storage rlk:tune ids append value "skyward_verse"
# 초월 · 악요개안: 협동 공격 피해 계수 · 재사용 대기(틱) · 원소 에너지 1pt당 폭발 피해 증가(0.01% 단위, 단계별 0.15/0.2/0.25/0.3%). 캐릭터별 원소 에너지 #burstCost 는 고정 · 반경 3칸 고정
data modify storage rlk:tune t.stormy_eye set value [{n:"#eyeCoef",m:"a"},{n:"#eyeCdT",m:"c"},{n:"#eyeRate",m:"a"}]
data modify storage rlk:tune ids append value "stormy_eye"
