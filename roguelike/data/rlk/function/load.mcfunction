# 로그라이크 시스템 - 초기 로드
data modify storage rlk:config installed set value 1b

# 표시(최종) 스탯: 체력·공격력·방어력은 자연수
scoreboard objectives add maxHealth dummy
scoreboard objectives add curHealth dummy
scoreboard objectives add moveSpeed dummy
scoreboard objectives add atkSpeed dummy
scoreboard objectives add critChance dummy
scoreboard objectives add critDamage dummy
scoreboard objectives add gold dummy

# 기본(base) 스탯
scoreboard objectives add base_maxHealth dummy
scoreboard objectives add base_moveSpeed dummy
scoreboard objectives add base_atkSpeed dummy
scoreboard objectives add base_critChance dummy
scoreboard objectives add base_critDamage dummy

# 장비(eq) 보너스
scoreboard objectives add eqMoveSpeed dummy
scoreboard objectives add eqAtkSpeed dummy
scoreboard objectives add eqCritChance dummy
scoreboard objectives add eqCritDamage dummy

# 증폭(×) 누산기

# 내부용
scoreboard objectives add init dummy
scoreboard objectives add pid dummy
scoreboard objectives add hpMaxPrev dummy
scoreboard objectives add tmp dummy
scoreboard objectives add lcSeen dummy
scoreboard objectives add pkbT dummy
scoreboard objectives add life dummy
scoreboard objectives add devMode dummy
scoreboard objectives add uiHash dummy
scoreboard objectives add scanTick dummy
scoreboard objectives add manageTick dummy
scoreboard objectives add invDirty dummy
# 아이템 보유 칸 수 (9 = 둘째 줄, 최대 18 = 셋째 줄까지). 인벤토리 슬롯 노드가 2칸씩 연다
scoreboard objectives add invCap dummy
scoreboard objectives add invEvt dummy
scoreboard objectives add invCnt dummy
# 장비 스캔의 빠른 길: 플레이어 = 마지막 스캔 번호, #scEp = 전체 스캔 번호(items/equip_scan · items/scan_fast)
scoreboard objectives add eqEp dummy
scoreboard objectives add hudHold dummy

# 전투/조작
scoreboard objectives add atkCD dummy
scoreboard objectives add comboStep dummy
scoreboard objectives add cboIdle dummy
# 평타 휘두르기 느려짐(player/swing/tick) · 1인칭 점프 통계(평타 사이 간격에서 뛰면 다음 평타는 1타부터)
scoreboard objectives add swCut dummy
scoreboard objectives add swHold dummy
scoreboard objectives add swJump minecraft.custom:minecraft.jump
scoreboard objectives add swungAt dummy
scoreboard objectives add intOwner dummy
scoreboard objectives add msid dummy

# 닷지(우클릭; 옛 대쉬의 이동 · 재사용 대기) · 패링(F) — 전투 개편 C (player/def/)
# dashCool = 닷지 재사용 대기(틱), dashInvT = 대쉬가 아닌 무적(원소폭발 시전 · 로노바 부활 · 추락 뒤; 닷지는 쓰지 않음)
# 시각(gametime) 도장: parAt 받은 F · parLk 이때까지 F 무시 · parHit 그 F 로 막은 틱 · dgAt 닷지 시작 · dgRw 보상을 준 닷지
scoreboard objectives add dashCool dummy
scoreboard objectives add parAt dummy
scoreboard objectives add parLk dummy
scoreboard objectives add parHit dummy
scoreboard objectives add dgAt dummy
scoreboard objectives add dgRw dummy
# 전투 개편 C 의 전역 값(#now 이번 틱 gametime, #dgOpen 퍼펙트 닷지 창이 열림, #dgEnd · #dgKill · #dgBox 시작 자리 상자, 섬광 간격,
# #parWs 헛누름 연속 · #parMl 무시한 F 뒤 받지 않는 끝, #dgRf 재사용 대기를 돌려준 닷지, #dgTry 마지막 닷지 시도)
scoreboard objectives add cb dummy
scoreboard players add #parWs cb 0
scoreboard players add #dgBox cb 0
execute unless score #parMl cb matches -2147483648.. run scoreboard players set #parMl cb -1000000
execute unless score #dgRf cb matches -2147483648.. run scoreboard players set #dgRf cb -1000000
execute unless score #dgTry cb matches -2147483648.. run scoreboard players set #dgTry cb -1000000
# 피해 문맥(한 번 쓰고 지움, player/def/judge): 비어 있는 값으로
scoreboard players set #hcK tmp 0
scoreboard players set #hcC tmp 0
scoreboard players set #hcNP tmp 0
scoreboard players set #hcND tmp 0
scoreboard players set #parT tmp 0
scoreboard players set #pdg tmp 0
scoreboard objectives add dashInvT dummy
scoreboard objectives add dashMoveT dummy
scoreboard objectives add dashPX dummy
scoreboard objectives add dashPZ dummy
scoreboard objectives add dashDX dummy
scoreboard objectives add dashDZ dummy
scoreboard objectives add dashUX dummy
scoreboard objectives add dashUZ dummy

# 몹
scoreboard objectives add stunT dummy
scoreboard objectives add burnI dummy
scoreboard objectives add frzT dummy

# 드롭 아이템 / 상점
scoreboard objectives add dgid dummy
scoreboard objectives add dprice dummy
scoreboard objectives add dopenT dummy
scoreboard objectives add aimingDrop dummy
scoreboard objectives add shopGid dummy
scoreboard objectives add shopOpenT dummy

# 아이템 스택/타이머
scoreboard objectives add kirionKills dummy
scoreboard objectives add pdStack dummy
scoreboard objectives add pdT dummy
scoreboard objectives add kirionFxT dummy
scoreboard objectives add bookPages dummy
scoreboard objectives add forbPages dummy
scoreboard objectives add fbMark dummy
scoreboard objectives add demonoBuff dummy
scoreboard objectives add demonoType dummy

# 디버그
scoreboard objectives add dbgPageCur dummy

# 공격력(물리·마법 통합): 최종 / 기본 / 장비 / 증폭
scoreboard objectives add atk dummy
scoreboard objectives add base_atk dummy
scoreboard objectives add ampAtk dummy

# 원소 부착 게이지(1000 = 1U) / 감쇠 속도
scoreboard objectives add aFire dummy
scoreboard objectives add aWater dummy
scoreboard objectives add aThunder dummy
scoreboard objectives add aIce dummy
scoreboard objectives add aGrass dummy
scoreboard objectives add dFire dummy
scoreboard objectives add dWater dummy
scoreboard objectives add dThunder dummy
scoreboard objectives add dIce dummy
scoreboard objectives add dGrass dummy

# 원소 상태(빙결·활성·연소·감전·초전도) / 부착 쿨 / 예약 반응
scoreboard objectives add quickT dummy
scoreboard objectives add burnOn dummy
scoreboard objectives add burnDmg dummy
scoreboard objectives add ecI dummy
scoreboard objectives add ecDmg dummy
scoreboard objectives add scT dummy
scoreboard objectives add icdT dummy
scoreboard objectives add icdC dummy
scoreboard objectives add rxQ dummy
scoreboard objectives add rxDmg dummy
scoreboard objectives add rxDmg3 dummy
scoreboard objectives add rxEl dummy
scoreboard objectives add elAct dummy
scoreboard objectives add icKey dummy

# 플레이어 원소(부여·피격 원소·방어막) / 원소 마스터리
scoreboard objectives add infuse dummy
scoreboard objectives add infuseT dummy
scoreboard objectives add hurtElem dummy
scoreboard objectives add shieldHP dummy
scoreboard objectives add shieldT dummy
scoreboard objectives add elemMastery dummy
scoreboard objectives add base_elemMastery dummy
scoreboard objectives add eqElemMastery dummy

# 레벨 / 경험치 / 사파이어
scoreboard objectives add level dummy
scoreboard objectives add xp dummy
scoreboard objectives add xpNeed dummy
scoreboard objectives add xpDrop dummy
scoreboard objectives add sapphire dummy
# 주사위(레벨 업 아이템 선택의 리롤권, 런마다 0) · 생명력 노드로 늘어난 최대 체력 %(런마다 0)
scoreboard objectives add dice dummy
scoreboard objectives add nodeHp dummy
# 월하대작(특수 보스 홍련의 이벤트 버프: 0 없음 · 1 켜짐, 런마다 0 = player/reset_one)
scoreboard objectives add hrMoon dummy
# 아이템 강화 단계 (가짜 플레이어 = 아이템 id, 0~3. rlk:pinv enh 와 같음)
scoreboard objectives add enhL dummy

# 방어력 · 깡/% 누산기(작업용) / 장비 보너스
scoreboard objectives add def dummy
scoreboard objectives add base_def dummy
scoreboard objectives add atkPct dummy
scoreboard objectives add atkFlat dummy
scoreboard objectives add hpPct dummy
scoreboard objectives add hpFlat dummy
scoreboard objectives add defPct dummy
scoreboard objectives add defFlat dummy
scoreboard objectives add eqAtkPct dummy
scoreboard objectives add eqAtkFlat dummy
scoreboard objectives add eqHpPct dummy
scoreboard objectives add eqHpFlat dummy
scoreboard objectives add eqDefPct dummy
scoreboard objectives add eqDefFlat dummy

# 체력 처리
scoreboard objectives add dead dummy
scoreboard objectives add hpKey dummy

# 방 시스템: 진행 상태(room) / 구역 표식 / 문 표식 / 오브젝트 / 경험치 샘
scoreboard objectives add room dummy
scoreboard objectives add zid dummy
scoreboard objectives add zkind dummy
scoreboard objectives add zst dummy
scoreboard objectives add ex0 dummy
scoreboard objectives add ex1 dummy
scoreboard objectives add ez0 dummy
scoreboard objectives add ez1 dummy
scoreboard objectives add da dummy
scoreboard objectives add db dummy
scoreboard objectives add dst dummy
scoreboard objectives add dvis dummy
scoreboard objectives add oact dummy
scoreboard objectives add oarg dummy
scoreboard objectives add ogid dummy
scoreboard objectives add xpLeft dummy
scoreboard objectives add xpPulse dummy

# 바닐라 체력 고정값 적용 여부
scoreboard objectives add vhp dummy

# 봉인 무늬(선 번호 / 등장 지연 / 타이머 / 단계)
scoreboard objectives add sidx dummy
scoreboard objectives add sdelay dummy
scoreboard objectives add sT dummy
scoreboard objectives add sph dummy

# 바닥 물결(중심 / 반지름)
scoreboard objectives add wx dummy
scoreboard objectives add wz dummy
scoreboard objectives add wr dummy

# 캐릭터: 재사용 대기 / 원소 에너지(×100, pt) / 표시 키 / 원소 충전 효율
scoreboard objectives add skillCd dummy
scoreboard objectives add burstCd dummy
scoreboard objectives add energy dummy
scoreboard objectives add energyPt dummy
scoreboard objectives add skShown dummy
scoreboard objectives add buShown dummy
scoreboard objectives add enKey dummy
scoreboard objectives add energyRecharge dummy
scoreboard objectives add base_energyRecharge dummy
scoreboard objectives add eqEnergyRecharge dummy

# 원소 입자 / 루미네(차가운 별빛·투창)
scoreboard objectives add pcVal dummy
scoreboard objectives add starlight dummy
scoreboard objectives add javQ dummy
scoreboard objectives add javT dummy
scoreboard objectives add javN dummy
scoreboard objectives add javBonus dummy
scoreboard objectives add jdmg dummy
scoreboard objectives add jcrit dummy
scoreboard objectives add lumP dummy

# 몬스터 레벨(mlv) / 1레벨 체력 / 맞은 몹의 레벨
scoreboard objectives add mlv dummy
scoreboard objectives add mhp0 dummy
scoreboard objectives add hurtLv dummy

# 초월 · 악요개안
scoreboard objectives add eyeCd dummy

# 초월 · 악요개안: 눈 움직임
scoreboard objectives add eyeAnim dummy

# 웅크림 감지(통계)
scoreboard objectives add sneakT minecraft.custom:minecraft.sneak_time

# 레벨 업 아이템 선택: 남은 횟수 / 모드 / 고른 선택지 / 조준 대상 / 다시 그리기 / 요소 종류·번호
scoreboard objectives add pkPending dummy
scoreboard objectives add pkMode dummy
scoreboard objectives add pkSel dummy
scoreboard objectives add pkHK dummy
scoreboard objectives add pkHI dummy
scoreboard objectives add pkRedraw dummy
scoreboard objectives add pkCd dummy
scoreboard objectives add pkKind dummy
scoreboard objectives add pkIdx dummy

# 각인 창 계산용(이름 = 각인 id)
scoreboard objectives add engCur dummy
scoreboard objectives add engAdd dummy
scoreboard objectives add engSub dummy

# 시점 시스템(숄더뷰): 설정·계산용(#이름) / 아바타 번호 / 몹의 지난 위치(어그로 다시 끌기 판단)
scoreboard objectives add view dummy
scoreboard objectives add avId dummy

# UI 클릭 직후 중복 인식 방지
scoreboard objectives add uiCd dummy

# 숄더뷰 회전 예측용(지난 틱의 좌우 각도 × 100)
scoreboard objectives add vYaw dummy

# 숄더뷰: 지난 틱의 상하 각도 × 100
scoreboard objectives add vPitch dummy

# 페보니우스 비전: 마지막으로 판정한 틱 / 쿨타임
scoreboard objectives add favAt dummy
scoreboard objectives add favCd dummy

# 숄더뷰: 지난 틱의 시선 변화량(좌우 / 상하)
scoreboard objectives add vDy dummy
scoreboard objectives add vDp dummy

# 각인: 계산용(#이름) / 개수(이름 = 각인 id) / 시험용 추가 개수 / 수호 보호막량·재생 대기
scoreboard objectives add eng dummy
scoreboard objectives add engN dummy
scoreboard objectives add engDev dummy
scoreboard objectives add gShield dummy
scoreboard objectives add gCd dummy

# 각인: 예리(확정 치명타 예약·쿨타임) / 광전사(공격 속도 지속)
scoreboard objectives add keenNext dummy
scoreboard objectives add keenCd dummy
scoreboard objectives add berT dummy

# 골드 조각에 담긴 골드
scoreboard objectives add gval dummy

# 아이템: 계산·타이머용(#이름) / 치유의 부적이 붙은 시각(몹)
scoreboard objectives add itv dummy
scoreboard objectives add talEnd dummy

# 인벤토리 상세: 판매 되묻기
scoreboard objectives add pkConf dummy

# 아이템 2차: 예약 표식의 종류·값 / 몹에 붙는 표시가 끝나는 시각(씨앗·거울·침식)
scoreboard objectives add iqK dummy
scoreboard objectives add skEnd dummy
scoreboard objectives add mirEnd dummy
scoreboard objectives add erodeEnd dummy

# 아이템 3차: 징조가 끝나는 시각(몹)
scoreboard objectives add omenEnd dummy

# 각인 표시: 놓여 있어야 할 각인 아이템의 총 개수
scoreboard objectives add engItems dummy

# 레벨 업 아이템 선택: 교체하려고 고른 보유 아이템의 순번
scoreboard objectives add pkSwap dummy

# 몹 체력(스코어): 현재 / 최대
scoreboard objectives add mhpC dummy
scoreboard objectives add mhpM dummy

# 피해 보너스(물리·원소별): 최종 / 장비
scoreboard objectives add physBonus dummy
scoreboard objectives add pyroBonus dummy
scoreboard objectives add hydroBonus dummy
scoreboard objectives add electroBonus dummy
scoreboard objectives add cryoBonus dummy
scoreboard objectives add geoBonus dummy
scoreboard objectives add anemoBonus dummy
scoreboard objectives add dendroBonus dummy
scoreboard objectives add eqPhysBonus dummy
scoreboard objectives add eqPyroBonus dummy
scoreboard objectives add eqHydroBonus dummy
scoreboard objectives add eqElectroBonus dummy
scoreboard objectives add eqCryoBonus dummy
scoreboard objectives add eqGeoBonus dummy
scoreboard objectives add eqAnemoBonus dummy
scoreboard objectives add eqDendroBonus dummy

# 레벨 업 선택: 이번 선택에서 리롤한 횟수
scoreboard objectives add pkRr dummy

# 투사체(로노바의 구체 · 잔향, char/bow/arrow_*): 종류 / 원소 / 틱당 이동 횟수 / 수명 / 부착 쿨
scoreboard objectives add aKind dummy
scoreboard objectives add aEl dummy
scoreboard objectives add aSub dummy
scoreboard objectives add aLife dummy
scoreboard objectives add aIcd dummy

# 스커크: 일곱빛 섬광 남은 틱 / 빠른 이동 남은 틱 / 고갈 남은 횟수 · 피해 증가% · 간격 / 3타의 두 번째 참격 예약 / 멸 진행 틱 · 초과한 뱀의 계략(pt)
scoreboard objectives add skM dummy
scoreboard objectives add skDash dummy
scoreboard objectives add skDep dummy
scoreboard objectives add skDepB dummy
scoreboard objectives add skDepCd dummy
scoreboard objectives add skQ dummy
scoreboard objectives add skBurst dummy
scoreboard objectives add skPts dummy

# 아이템 도감: 탭 / 쪽
scoreboard objectives add cxTab dummy
scoreboard objectives add cxPage dummy

# 생명의 계약
scoreboard objectives add bol dummy

# 근접 공통: 두 번째 참격 예약 · 그 계수
scoreboard objectives add naQ dummy
scoreboard objectives add naQc dummy

# 클로린드: 밤 순찰 남은 틱 / 밤 꿰뚫기 간격 / 원소폭발 진행 / 고유 특성 스택 · 남은 틱
scoreboard objectives add clNV dummy
scoreboard objectives add clLCd dummy
scoreboard objectives add clBurst dummy
scoreboard objectives add clP dummy
scoreboard objectives add clPT dummy

# 아를레키노: 붉은 죽음의 가면(0/1) / 핏값이 끝나는 시각(몹)
scoreboard objectives add arM dummy
scoreboard objectives add arDir dummy

# 일반 공격 모션 · 생명의 계약 HUD
scoreboard objectives add fxId dummy
scoreboard objectives add fxT dummy
scoreboard objectives add bolKey dummy

# 아를레키노 스킬 대기
scoreboard objectives add arSk dummy

# 살짝 전진 남은 틱
scoreboard objectives add stepT dummy

# 클로린드 원소 입자 간격 · 개수
scoreboard objectives add clPcCd dummy
scoreboard objectives add clPcN dummy

# 클로린드 자동 연사 / 원소폭발 시전 동작
scoreboard objectives add clAuto dummy
scoreboard objectives add clTg dummy
scoreboard objectives add buT dummy

# 나비아: 결정 축포 충전 · 충전 진행 · 실제 충전 시간 · 결정 파편 · 파편 남은 시간 · 고유 특성 · 원소폭발 지속 · 포격 간격 · 포격 파편 간격 · 조준 · 조준 신호 간격 · 연속 발사 방지 · 우산총 표시 · 맞은 장미탄 수 / 근접 추가 타격 수
scoreboard objectives add nvC dummy
scoreboard objectives add nvCT dummy
scoreboard objectives add nvCdE dummy
scoreboard objectives add nvS dummy
scoreboard objectives add nvST dummy
scoreboard objectives add nvP dummy
scoreboard objectives add nvQ dummy
scoreboard objectives add nvQT dummy
scoreboard objectives add nvQS dummy
scoreboard objectives add nvA dummy
scoreboard objectives add nvGap dummy
scoreboard objectives add nvFcd dummy
scoreboard objectives add nvGun dummy
# 나비아: 결정 축포 발사 대기(모션의 발사 틱 전)
scoreboard objectives add nvShot dummy
scoreboard objectives add nvHit dummy
scoreboard objectives add naQn dummy

# 도감 시작 모드(런 시작 아이템 고르기)
scoreboard objectives add cxMode dummy

# 나비아 결정 파편 표시: 만든 개수 · 칸 번호 · 직전 개수
scoreboard objectives add nvShK dummy
scoreboard objectives add nvShI dummy
scoreboard objectives add nvShP dummy

# 로노바 · 공허: 공허 부착 · 감쇠 · 잠식 · 잠식 유지 시간 · 재연 반응 제외 시간 · 몹 번호 · 파편 대상 · 잔향 3칸 · 잔향 수 · 잔향 표시 키 · 표시 칸 · 재연 간격 · 원소폭발 진행 · 불사의 저주 사용
scoreboard objectives add aVoid dummy
scoreboard objectives add dVoid dummy
scoreboard objectives add rnEr dummy
scoreboard objectives add rnErT dummy
scoreboard objectives add rnNoE dummy
scoreboard objectives add rnId dummy
scoreboard objectives add rnTg dummy
scoreboard objectives add rnE1 dummy
scoreboard objectives add rnE2 dummy
scoreboard objectives add rnE3 dummy
scoreboard objectives add rnEn dummy
scoreboard objectives add rnEcK dummy
scoreboard objectives add rnEcI dummy
scoreboard objectives add rnFcd dummy
scoreboard objectives add rnQ dummy
scoreboard objectives add rnRev dummy
scoreboard objectives add snd dummy

# 숄더뷰: 공격·스킬 뒤 조준선을 보는 남은 시간
scoreboard objectives add vAimT dummy

# 로노바: 불사의 저주로 쓰러져 있는 남은 시간
scoreboard objectives add rnDie dummy

# 화면 제목: 다른 제목이 떠 있는 남은 시간 · 아이템 선택 안내 다시 띄우기까지
scoreboard objectives add ttlT dummy
scoreboard objectives add pkSubT dummy

# 아를레키노: 핏값 표식 조각의 가운데 위치(몹마다, × 0.001칸)
scoreboard objectives add armY dummy
scoreboard objectives add armZ dummy

# 달 반응: 달 감전 표시 · 달 개화 · 달 결정 예약 · 월광 결정 간격
scoreboard objectives add lnEC dummy
scoreboard objectives add lnBloom dummy
scoreboard objectives add lnCr dummy
scoreboard objectives add lnI dummy

# 네페르: 스킬 충전 · 충전 진행 · 실제 충전 시간 · 연속 사용 방지 · 그림자 춤 · 환영극 횟수 · 환영극 진행 · 원소폭발 진행 · 폭발 때 장막 · 풀 이슬 · 이슬 창 · 이슬 진행 · 기만의 장막 · 장막 시간 · 이슬 표시 키 · 표시 칸 · 이전 개수
scoreboard objectives add nfC dummy
scoreboard objectives add nfCT dummy
scoreboard objectives add nfCdE dummy
scoreboard objectives add nfFcd dummy
scoreboard objectives add nfSD dummy
scoreboard objectives add nfPh dummy
scoreboard objectives add nfPT dummy
scoreboard objectives add nfQ dummy
scoreboard objectives add nfQV dummy
scoreboard objectives add nfDew dummy
scoreboard objectives add nfDewW dummy
scoreboard objectives add nfDewT dummy
scoreboard objectives add nfVeil dummy
scoreboard objectives add nfVeilT dummy
scoreboard objectives add nfDwK dummy
scoreboard objectives add nfDwI dummy
scoreboard objectives add nfDwP dummy

# 풀 원핵 비행: 시작 · 도착 좌표(× 1000) · 진행 틱
scoreboard objectives add cX0 dummy
scoreboard objectives add cY0 dummy
scoreboard objectives add cZ0 dummy
scoreboard objectives add cX1 dummy
scoreboard objectives add cY1 dummy
scoreboard objectives add cZ1 dummy
scoreboard objectives add cF dummy

# 결정 방어막의 원소(같은 원소 피해를 250% 효율로 막음)
scoreboard objectives add shieldEl dummy

# 살롱의 초대장: 멤버 번호(0 우셰르 · 1 슈발마린 · 2 크라발레타)
scoreboard objectives add smI dummy

# 대쉬: 이번 대쉬에서 단차를 넘은 횟수
scoreboard objectives add dashUpN dummy

# 로노바: 잔향 얻기 대기(틱)
scoreboard objectives add rnEcd dummy

# 로비: 계산 · 상태(#tutS 튜토리얼 단계 · #dps* DPS · #lobInf · #lobAura)
scoreboard objectives add lob dummy

# 로비 오브젝트: 묶음 번호 · 동작
scoreboard objectives add lgid dummy
scoreboard objectives add lact dummy

# 로비: 지금 있는 방(1 로비 · 2 튜토리얼 · 3 설정 · 4 체험)
scoreboard objectives add lobRoom dummy
# 접속 끊음 횟수(다시 접속하면 로비로)
scoreboard objectives add rlkLeave minecraft.custom:minecraft.leave_game

# 커스텀 몹(cm): 연결 번호 · 상태 · 타이머 · 쿨 · 바라보는 방향 · 방패 · 투사체 값
scoreboard objectives add cmId dummy
scoreboard objectives add cmS dummy
scoreboard objectives add cmT dummy
scoreboard objectives add cmCd dummy
scoreboard objectives add cmCd2 dummy
scoreboard objectives add cmF dummy
scoreboard objectives add cmYaw dummy
scoreboard objectives add cmSh dummy
scoreboard objectives add cmShM dummy
scoreboard objectives add cmN dummy
scoreboard objectives add cmD dummy
scoreboard objectives add cmD2 dummy
scoreboard objectives add cmLv dummy
scoreboard objectives add cmEl dummy
scoreboard objectives add cmV dummy
scoreboard objectives add cmVx dummy
scoreboard objectives add cmVy dummy
scoreboard objectives add cmVz dummy
scoreboard objectives add cmPx dummy
scoreboard objectives add cmPy dummy
scoreboard objectives add cmPz dummy

# 시점: 다른 제목 글자가 떠 있는 동안 조준점 쉬기

# 시점: 큰 제목이 떠 있는 동안 조준점 쉬기 · 지난 틱의 ttlT
scoreboard objectives add vBig dummy
scoreboard objectives add vTtp dummy

# F5 위쪽 시점: 웅크리기 직전 상태 · 우클릭(사용 중) 표시 · 누른 틱 수
scoreboard objectives add vSnk dummy
scoreboard objectives add rcU dummy
scoreboard objectives add rcT dummy

scoreboard objectives add rlkMenu trigger
# 지도 화면: 여는 중 · 연 뒤 틱 · 4번 칸을 들고 있던 직전 상태
scoreboard objectives add vMap dummy
scoreboard objectives add vMapT dummy
scoreboard objectives add vMapH dummy

scoreboard objectives add dbgDropI trigger
scoreboard objectives add dbgPage trigger
# 스택 사이드바 (아이템 스택/카운트 표시)
scoreboard objectives add stacks dummy {"text":"스택","color":"gold"}
scoreboard objectives setdisplay sidebar stacks

# 이전 버전에서 쓰던 스코어보드 정리(없으면 무시됨)
scoreboard objectives remove physAtk
scoreboard objectives remove magicAtk
scoreboard objectives remove base_physAtk
scoreboard objectives remove base_magicAtk
scoreboard objectives remove eqPhysAtk
scoreboard objectives remove eqMagicAtk
scoreboard objectives remove ampPhysAtk
scoreboard objectives remove ampMagicAtk
scoreboard objectives remove baseMagic
scoreboard objectives remove poisT
scoreboard objectives remove poisD
scoreboard objectives remove poisI
scoreboard objectives remove poisInt
scoreboard objectives remove wound
scoreboard objectives remove burnT
scoreboard objectives remove burnD
scoreboard objectives remove burnNbMul
scoreboard objectives remove burnArson
scoreboard objectives remove burnMag
scoreboard objectives remove frzHits
scoreboard objectives remove frzAz4
scoreboard objectives remove stnT
scoreboard objectives remove hbCol
scoreboard objectives remove dmgAmp
scoreboard objectives remove dmgAmpT
scoreboard objectives remove defense
scoreboard objectives remove base_defense
scoreboard objectives remove eqMaxHealth
scoreboard objectives remove eqDefense
scoreboard objectives remove baseAtk
scoreboard objectives remove hpPrevH
scoreboard objectives remove hpSyncS
scoreboard objectives remove eqAtk
scoreboard objectives remove iqV

# 죽어도 인벤토리를 떨구지 않음(아이템·UI 아이템이 쏟아지지 않게)
gamerule keep_inventory true
scoreboard objectives remove vpx
scoreboard objectives remove vpz

scoreboard players set #c4 tmp 4
scoreboard players set #10000 tmp 10000
scoreboard players set #c8 tmp 8
scoreboard players set #c3 tmp 3
scoreboard players set #c110 tmp 110
scoreboard players set #c300 tmp 300
scoreboard players set #c12 tmp 12
scoreboard players set #c83 tmp 83
scoreboard players set #c15 tmp 15
scoreboard players set #c30 tmp 30
scoreboard players set #c360 tmp 360
scoreboard players set #c130 tmp 130
scoreboard players set #c160 tmp 160
scoreboard players set #c175 tmp 175
scoreboard players set #c600 tmp 600
scoreboard players set #c2 tmp 2
scoreboard players set #c10 tmp 10
scoreboard players set #10 tmp 10
scoreboard objectives remove vTtl

# ===== 조절 지점 =====
# rift (build_rift.py)
scoreboard players set #riftPm room 30
# 로비 · 튜토리얼 · 설정 · 체험 방(lobby/): 항상 불러와 둠
forceload add 80 14 134 64
scoreboard players set #c2 lob 2
scoreboard players set #c5 lob 5
scoreboard players set #c20 lob 20
scoreboard players set #c40 lob 40
# 시작 아이템 개수: 지금은 1개 고정(나중에 사파이어로 해금)
data modify storage rlk:config start_picks set value 1
# 결정 방어막: 같은 원소 피해를 막는 효율(%)
scoreboard players set #shElEff tmp 250
# 아를레키노 스킬(재가 된 만상): 맞은 적 경직(틱) · 넉백(칸/틱 × 1000)
scoreboard players set #arSkStun tmp 12
scoreboard players set #arSkKb tmp 550
# 풀 원핵이 날아가는 시간(틱) · 포물선 높이(× 0.001칸 ÷ 4 를 시간² 로 나눈 값: 36 = 10틱일 때 0.9칸)
scoreboard players set #cN tmp 10
scoreboard players set #cArc tmp 36
# 각인 만월: (2) 달 반응 피해 +% · (4) 원소 마스터리 · 지속(틱)
scoreboard players set #fmDmg tmp 15
scoreboard players set #fmEm tmp 80
scoreboard players set #fmDur tmp 160
# 월하대작(특수 보스 홍련의 이벤트 버프): 최종 공격력 +% · 치명타 확률 +% · 이동 속도 +% (아이템이 아니라 강화와 상관없음) · 범위
#   #hrMoonRun 1 = 이번 런(player/reset_one 이 끄고 스탯 줄 "(이번 런)") / 0 = 영구(끄지 않고 "(영구)"). 영구로 바꾸려면 여기서
#   8 · 4 · 4 와 #hrMoonRun 0, 그리고 tools/mboss_scarlet/api.py 의 EVENT['buff_scope'] = 'forever'(균열 채팅 문구; 재생성) (계획 §7.5.3)
scoreboard players set #hrMoonAtk tmp 27
scoreboard players set #hrMoonCrit tmp 10
scoreboard players set #hrMoonSpd tmp 10
scoreboard players set #hrMoonRun tmp 1
# 서리달의 은잔: 중력의 물결 시간(틱) · 피해(최대 체력 ‰) · 중력 1번 · 발동 기준 · 중력 간섭(반응 기준 %) · 월광 시간(틱) · 월광 달 피해 +%
scoreboard players set #cgRipDur tmp 500
scoreboard players set #cgRipPm tmp 35
scoreboard players set #cgGain tmp 20
scoreboard players set #cgMax tmp 60
scoreboard players set #cgGI tmp 300
scoreboard players set #cgMoonDur tmp 240
scoreboard players set #cgMoon tmp 15
# 네페르: 기본 원소 마스터리 보너스 · 스킬 충전 시간(틱) · 그림자 춤(틱) · 풀 이슬 간격(틱 × 100, 모래의 딸 보너스로 빨라짐) · 기만의 핵 시간(틱) · 기만의 장막 시간(틱)
scoreboard players set #nfEm tmp 100
scoreboard players set #nfCd tmp 240
scoreboard players set #nfSDT tmp 180
scoreboard players set #nfDewGap tmp 5000
scoreboard players set #nfDecDur tmp 300
scoreboard players set #nfVeilDur tmp 160
# 달 반응: 달 감전 1초 피해 · 달 결정의 월광 결정 한 발 · 달 개화(이름 표시용) — 반응 기준(공격력 × #reactBase%) 의 %
scoreboard players set #lnEC tmp 180
scoreboard players set #lnCR tmp 120
# 로노바 명계의 반동(부활 충격파): 피해 계수는 char/ronova/rev_wave(250%) · 반경 6칸 · 잠식 +20% · 밀어내는 세기(칸/틱 × 1000)
scoreboard players set #rnRevKb tmp 1300
# 로노바 불사의 저주: 쓰러져 있는 시간(틱) · 되살아난 체력(최대 체력의 %)
scoreboard players set #rnDieT tmp 60
scoreboard players set #rnRevPct tmp 30
# 숄더뷰: 이동할 때 몸을 돌리는 최대 속도(틱당 각도 × 100) · 공격/스킬 뒤 조준선을 계속 보는 시간(틱)
scoreboard players set #viewTurn tmp 4500
scoreboard players set #viewAimHold tmp 15
# 로노바 · 공허: 공허 공격 1회의 잠식(%) · 잠식 최대(%) · 마지막 공허 공격 뒤 잠식이 줄기 시작하는 시간(틱, 그 뒤 1초에 1%) · 재연 간격(틱) · 일반 공격 간격(틱, 4타 뒤). 계수는 char/ronova/na
scoreboard players set #rnErHit tmp 2
scoreboard players set #rnErMax tmp 20
scoreboard players set #rnErHold tmp 100
scoreboard players set #rnGap tmp 40
# 로노바: 잔향을 얻은 뒤 다음 잔향을 얻을 수 있기까지(틱)
scoreboard players set #rnEcdT tmp 40
scoreboard players set #rnNaCd tmp 10
scoreboard players set #rnNaCd4 tmp 16
scoreboard players set #c25 tmp 25
scoreboard players set #c256 tmp 256
scoreboard players set #c200 tmp 200
# 런 시작 때 고르는 아이템 개수(커먼·레어 중). 나중에 사파이어로 늘리려면 이 저장소 값을 바꾼다
execute unless data storage rlk:config start_picks run data modify storage rlk:config start_picks set value 1
# 나비아: 장미탄 기본 피해(공격력의 %) · 결정 축포 충전 시간(틱) · 결정 파편 최대 개수 · 지속(틱) · 고유 특성 지속(틱) · 그동안 일반 공격 피해 증가(%)
scoreboard players set #nvBase tmp 450
scoreboard players set #nvCd tmp 180
scoreboard players set #nvMax tmp 6
scoreboard players set #nvDur tmp 6000
scoreboard players set #nvPDur tmp 80
scoreboard players set #nvPBonus tmp 40
#   원소폭발: 지원 포격 지속(틱) · 간격(틱) · 포격으로 결정 파편을 얻는 간격(틱). 피해 계수는 char/navia/burst(120%) · q_shot(65%)
scoreboard players set #nvQDur tmp 240
scoreboard players set #nvQGap tmp 15
scoreboard players set #nvQSh tmp 48
# 원소폭발 시전 동작: 버튼을 누른 뒤 발동까지(틱) · 발동 뒤에도 이어지는 무적(틱)
scoreboard players set #burstWind tmp 16
scoreboard players set #burstInv tmp 8
# 낙사 구간: 떨어졌을 때 플레이어가 입는 피해(최대 체력의 %). 이 피해로는 죽지 않는다(체력 1 은 남는다)
scoreboard players set #fallPct tmp 10
# 클로린드 밤 꿰뚫기 회복: 해소한 생명의 계약의 %(생명의 계약 100% 미만 / 이상) · 원소 입자 간격(틱) · 스킬 한 번에 최대 개수
scoreboard players set #clHeal tmp 2
scoreboard players set #clHeal2 tmp 3
scoreboard players set #clPcGap tmp 40
scoreboard players set #clPcMax tmp 4
# 클로린드 밤 꿰뚫기의 전진: 틱당 0.1칸 × #clStepSpd, #clStepT 틱 (5 × 4 = 2칸)
scoreboard players set #clStepSpd tmp 5
scoreboard players set #clStepT tmp 4
# 아를레키노: 붉은 죽음의 가면이 켜지는 생명의 계약(%) / 가면 중 일반 공격 추가 피해(공격력의 % × 생명의 계약%/100) / 적중 시 생명의 계약 소모(‰) · 스킬 재사용 대기 감소(틱) / 가면 중 불 원소 피해 보너스(%)
scoreboard players set #arMaskMin tmp 30
scoreboard players set #arMaskCoef tmp 120
scoreboard players set #arUse tmp 75
scoreboard players set #arCdCut tmp 16
scoreboard players set #arPyro tmp 40
#   핏값 지속(틱) / 흡수 1개당 생명의 계약(%) · 흡수로 채울 수 있는 상한(%) / 원소폭발 회복: 해소한 생명의 계약의 % + 공격력의 %
scoreboard players set #arDirDur tmp 600
#   재가 된 만상: 사라져 있는 시간(틱)
scoreboard players set #arSkDelay tmp 7
scoreboard players set #arAbs tmp 65
scoreboard players set #arAbsMax tmp 145
scoreboard players set #arHealBol tmp 30
scoreboard players set #arHealAtk tmp 40
# 클로린드: 밤 순찰 지속(틱) / 사격 간격(공격 속도 100% 기준 틱×100) / 사격으로 얻는 생명의 계약(%) / 밤 꿰뚫기 사이 간격(틱) / 원소폭발로 얻는 생명의 계약(%) / 고유 특성 치명타 확률(스택당 %) · 지속(틱)
scoreboard players set #clDur tmp 180
scoreboard players set #clShotCd tmp 700
scoreboard players set #clShotBol tmp 35
scoreboard players set #clLungeCd tmp 20
scoreboard players set #clBurstBol tmp 66
scoreboard players set #clPCrit tmp 10
scoreboard players set #clPDur tmp 300
# 생명의 계약: 상한(최대 체력의 %)
scoreboard players set #bolMax tmp 200
# 각인 계약: (2) 생명의 계약이 있는 동안 공격력% / (4) 해소 뒤 주는 피해 증가% · 지속(틱)
scoreboard players set #pactAtk tmp 18
scoreboard players set #pactDmg tmp 25
scoreboard players set #pactDur tmp 160
# 스커크 (뱀의 계략 수치는 pt × 100)
#   스킬로 얻는 양 / 일곱빛 섬광 중 틱당 소모(25 = 초당 5pt) / 일곱빛 섬광 지속(틱) / 빠른 이동 지속(틱) · 그 뒤 재사용 대기(틱) · 숄더뷰 이동 속도(%)
scoreboard players set #skGain tmp 4500
scoreboard players set #skDrain tmp 25
scoreboard players set #skModeDur tmp 240
scoreboard players set #skDashDur tmp 60
scoreboard players set #skDashCd tmp 160
scoreboard players set #skDashSpd tmp 150
#   허계 균열: 흡수 1개당 얻는 양 / 생성 간격(틱) / 남아 있는 시간(틱) — 최대 3개, 흡수 범위 6칸은 char/skirk/absorb
scoreboard players set #skRiftGain tmp 800
scoreboard players set #skRiftCdT tmp 50
scoreboard players set #skRiftLife tmp 300
#   멸: 필요한 뱀의 계략 / 초과 1pt당 추가 피해(공격력의 % × 100) / 초과분 최대(pt) — 참격 계수 220·370 과 진의 8%·+4% 는 char/skirk/ 안
scoreboard players set #skBurstMin tmp 5000
scoreboard players set #skPtBonus tmp 3478
scoreboard players set #skPtMax tmp 12
# 기본 공격에 맞은 몹: 경직 시간(틱) / 밀려나는 세기(칸/틱 × 1000. 바닐라 넉백 = 400, 0 이면 안 밀림)
scoreboard players set #stunBasic tmp 2
scoreboard players set #kbBasic tmp 180
# 닷지(우클릭 · 옛 대쉬 이동): 재사용 대기(틱)의 기본값 — 누르면 #dashCoolBase(아무것도 피하지 못한 닷지), 그 닷지가 공격을 피하면(퍼펙트 ·
# 넓은 닷지) #dashCoolHitBase 가 되게 차이만큼 돌려준다(닷지 한 번에 한 번, player/def/dg_refund). 실제 값 #dashCoolT · #dashCoolHitT 는
# 각인(질주 2개: -#dashEngSpd %, 반올림)에 따라 engravings/scan_more 가 계산
scoreboard players set #dashCoolBase tmp 18
scoreboard players set #dashCoolHitBase tmp 12
scoreboard players set #dashCoolT tmp 18
scoreboard players set #dashCoolHitT tmp 12
# 닷지 창(누른 틱 = 0): #dgPW 틱 미만에 맞을 공격 = 퍼펙트 닷지(모든 적), #dgLW 틱 미만 = 일반 몹(#dgLooseC: 0 일반만, 1 정예까지)만 회피
scoreboard players set #dgPW tmp 3
scoreboard players set #dgLW tmp 7
scoreboard players set #dgLooseC tmp 1
# 퍼펙트 닷지: 원소 에너지(× 100, 고정량 · 원소 충전 효율 미적용)
scoreboard players set #dgEn tmp 1000
# 패링 창(F 를 받은 틱 = 0): #parW3 틱 미만 = 3단계(퍼펙트), #parW2 미만 = 2단계, #parW1 미만 = 1단계, 그 뒤 = 실패
scoreboard players set #parW3 tmp 3
scoreboard players set #parW2 tmp 6
scoreboard players set #parW1 tmp 10
# 받은 F 뒤 다시 받지 않는 시간(틱) = #parGap × (1 + 헛누름 연속 #parWs cb). 헛누름 연속: 받은 F 가 아무것도 막지 못한 채 창이 끝나고
# #parWsT 틱 안에 다음 F 를 받으면 +1(최대 #parWsMax: 12 → 24 → 36 → 48틱), 그보다 오래 쉬면 0, #parWsClr 단계 이상의 패링이 되면 0
# (2 = 2 · 3단계. 1단계 — 타이밍이 가장 안 맞은 패링 — 는 연속을 지우지 못한다; 1 이면 어느 단계든 지움)
scoreboard players set #parGap tmp 12
scoreboard players set #parWsMax tmp 3
scoreboard players set #parWsT tmp 80
scoreboard players set #parWsClr tmp 2
# 받지 않은 F(연타 · 키를 누르고 있어 생기는 반복 입력) 뒤 이 틱 수 동안은 어떤 F 도 받지 않는다(#parMl cb; 패링이 되어도 풀리지 않음:
# 3틱보다 빠른 연타는 처음 한 번만 받는다) / 패링이 된 뒤 다음 F 를 받기까지(틱; 연속 공격을 3틱 간격으로도 이어 막게)
scoreboard players set #parRe tmp 3
scoreboard players set #parChain tmp 1
# 2단계 · 1단계가 남기는 피해(%) / 퍼펙트 패링의 원소전투 스킬 재사용 대기 감소(틱)
scoreboard players set #parKeep2 tmp 20
scoreboard players set #parKeep1 tmp 50
scoreboard players set #parCut tmp 20
# 패링 불가 공격의 섬광: 같은 공격자에게 다시 띄우지 않는 간격(틱)
scoreboard players set #npGap tmp 10
# 기본공격 콤보 딜레이(공격속도 100% 기준 틱×100): 1타→2타, 2타→1타
scoreboard players set #comboD12 tmp 600
scoreboard players set #comboD21 tmp 1000
# 봉인된 검 → 마검: 키리온 변신에 필요한 처치 수 / 금단의 도서 → 데모노미콘 변신에 필요한 페이지 수
scoreboard players set #kirionNeed tmp 150
scoreboard players set #forbNeed tmp 250

# 액션바 HUD: 다른 액션바 안내(골드 부족 등)가 뜰 때 HUD 를 잠시 멈추는 시간(틱)
scoreboard players set #hudHoldT tmp 40

# 레벨: 1레벨 기초 수치 / 레벨당 증가량 / 필요 경험치(1레벨 → 2레벨) / 레벨당 필요 경험치 증가 / 몹 처치 경험치(몹의 xpDrop 스코어가 우선, 0 = 없음)
scoreboard players set #lvHp0 tmp 100
scoreboard players set #lvHpUp tmp 12
scoreboard players set #lvAtk0 tmp 10
scoreboard players set #lvAtkUp tmp 2
scoreboard players set #lvDef0 tmp 10
scoreboard players set #lvDefUp tmp 2
scoreboard players set #xpNeed0 tmp 40
scoreboard players set #xpNeedUp tmp 20
scoreboard players set #killXp tmp 4
# 몹 처치 골드: 최소 / 최대(× 챕터) / 보스 배율
scoreboard players set #mobGoldMin tmp 2
scoreboard players set #mobGoldMax tmp 4
scoreboard players set #bossGoldMul tmp 15
# 보스 처치 사파이어 개수
scoreboard players set #bossSapphire tmp 2
# 바닐라 체력 고정값 × 100 (player/init, player/vhp_fix 의 1024 과 같아야 함)
scoreboard players set #vhp100 tmp 102400
# 피격: 받는 원피해 = 바닐라 피해(하트 반 칸 = 1) × #mobDmgMul / 방어력 공식 = 원피해 × #defK / (#defK + 방어력)
scoreboard players set #mobDmgMul tmp 5
scoreboard players set #defK tmp 100
# 회복구슬: 최대 체력의 %
scoreboard players set #orbHealPct tmp 10
# 액션바 HP 바 칸 수 (바꾸면 p10 의 HPSEG 로 다시 만든 player/hud/setup 과 같아야 함)
scoreboard players set #hudHpSeg tmp 30

# 구역에 들어설 때 바닥이 바뀌는 물결의 속도(틱당 칸 수)
scoreboard players set #waveSpeed tmp 3
# 원소 입자 하나의 기본 원소 에너지 × 100: 캐릭터와 같은 원소 / 무속성 / 다른 원소 (원신은 3 / 2 / 1. 여기서는 입자를 만들어 줄 동료가 없어 4 / 2.7 / 1.3)
scoreboard players set #enSame tmp 400
scoreboard players set #enNeutral tmp 270
scoreboard players set #enOther tmp 130
# 액션바 원소 에너지 게이지 칸 수 (char/hud_setup 과 같아야 함)
scoreboard players set #hudEnSeg tmp 15
# 몬스터 레벨 (x = 레벨 - 1). 플레이어는 레벨이 오를수록 좋은 아이템을 얻으므로, 몹은 레벨에 따라 플레이어 기초 수치보다 빠르게 강해짐
#  체력 = 1레벨 체력 × (100 + #mobLvHp·x + #mobLvHp2·x²/100)%
#  공격 = 원피해 × (100 + #mobLvAtk·x + #mobLvAtk2·x²/100)%
#  방어: 플레이어 → 몹 레벨 보정의 몹 쪽 항 = 100 + 몹 레벨 × #mobLvDef/100 (플레이어 쪽 = 100 + 플레이어 레벨)
#  플레이어 방어 상수: 실제 피해 = 원피해 × K/(K + 방어력), K = #defK + #defKLv·(때린 몹 레벨 - 1)
scoreboard players set #mobLvHp tmp 30
scoreboard players set #mobLvHp2 tmp 5
# 모든 몹의 체력 배율(%). 400 = 4배. 몹이 너무 빨리/늦게 죽으면 이 숫자 하나만 바꾸면 됨
scoreboard players set #mobHpMul tmp 400
scoreboard players set #mobLvAtk tmp 14
scoreboard players set #mobLvAtk2 tmp 6
scoreboard players set #mobLvDef tmp 150
scoreboard players set #defKLv tmp 4
# 보스(나루카미) 공격 피해 배율(%). 레벨 보정과 별개로 곱함
scoreboard players set #bossDmgMul tmp 160

# 재련 맵을 한 판에 고를 수 있는 최대 횟수
scoreboard players set #rfMax tmp 2
# 시점 시스템(숄더뷰): 걷는 속도(칸/틱 × 10000, 이동 속도 100% 기준) / 달리기 배율(%)
scoreboard players set #viewWalk tmp 2159
scoreboard players set #viewSprint tmp 130
# 평타를 휘두르는 동안(swHold) 걷는 속도(%, 달리기 배율 없음). 숄더뷰 · F5 시점의 아바타(view/move). 1인칭은 걷기를 늦추지 않고
# 점프만 막는다(이동 속도 속성을 낮추면 바닐라가 화면을 확대함, player/swing/tick)
scoreboard players set #swSlow tmp 50
# 숄더뷰 카메라: 시선 고르게 펴기 보정의 한도(각도 × 100)
# 숄더뷰: 점프로 떠오른 높이 중 카메라가 따라가는 비율(%). 100 = 예전처럼 전부 따라감, 0 = 전혀 안 따라감
scoreboard players set #viewJump tmp 25
# 숄더뷰: 대쉬 중 카메라를 몇 틱에 걸쳐 옮길지(아바타가 화면에서 따라오는 속도 = 3) / 대쉬가 끝난 뒤에도 그 값을 유지하는 틱 수
scoreboard players set #viewDashDur tmp 3
scoreboard players set #viewDashHold tmp 8
scoreboard players set #viewEven tmp 300
scoreboard players set #2 tmp 2
# 페보니우스 비전: 발동 확률(%) / 회복하는 원소 에너지(pt × 100, 여기에 원소 충전 효율이 곱해짐) / 쿨타임(틱)
scoreboard players set #favChance tmp 60
scoreboard players set #favEnergy tmp 1000
scoreboard players set #favCdT tmp 160
# 각인 수치 (설명 글은 engravings/register 에 따로 적혀 있으니 같이 고칠 것)
#   개수 효과(스탯): #es_<각인><개수>
scoreboard players set #es_guard2 tmp 20
scoreboard players set #es_elemental2 tmp 10
scoreboard players set #es_unyielding2 tmp 10
scoreboard players set #es_amplify2 tmp 150
scoreboard players set #es_emblem2 tmp 35
scoreboard players set #es_keen2 tmp 8
scoreboard players set #es_keen4 tmp 30
scoreboard players set #es_dash1 tmp 5
scoreboard players set #es_execute2 tmp 10
scoreboard players set #es_flurry2 tmp 10
scoreboard players set #es_berserk2 tmp 12
#   수호: 보호막량 / 보호막이 있을 때 주는 피해 증가% / 깨진 뒤 재생까지(틱)
scoreboard players set #guardAmt tmp 100
scoreboard players set #guardDmg tmp 20
scoreboard players set #guardCdT tmp 300
#   원소: 심연의 원소 최대 스택 (탄환 피해 50% 는 engravings/abyss/fire)
scoreboard players set #abyssMax tmp 4
#   불굴: 체력 기준(%) / 주는 피해 증가%
scoreboard players set #unyHp tmp 40
scoreboard players set #unyDmg tmp 40
#   증폭: 증발·융해 피해 증가%
scoreboard players set #ampRx tmp 30
#   절연: 원소폭발 피해 += 원소 충전 효율 × N% (최대)
scoreboard players set #emblemPct tmp 25
scoreboard players set #emblemMax tmp 75
#   순환: 스킬 재사용 대기 감소% / 입자 하나당 줄어드는 틱
scoreboard players set #cycleCd tmp 15
scoreboard players set #cycleCut tmp 10
#   예리: 확정 치명타 쿨타임(틱)
scoreboard players set #keenCdT tmp 80
#   질주: 닷지 재사용 대기 감소% (닷지 통과 피해 80% 는 engravings/dash/hit)
scoreboard players set #dashEngSpd tmp 20
#   빙설: 얼음 원소 피해 증가% / 빙결된 적 치명타 확률 증가(%p)
scoreboard players set #frostDmg tmp 15
scoreboard players set #frostCrit tmp 40
#   처형: 적 체력 기준(%) / 주는 피해 증가%
scoreboard players set #execHp tmp 30
scoreboard players set #execDmg tmp 40
#   보물: 골드 획득 증가% / 골드 몇당 공격력 1% / 최대 공격력%
scoreboard players set #treasureGold tmp 20
scoreboard players set #treasurePer tmp 100
scoreboard players set #treasureMax tmp 30
#   연격: 추가타 계수(%)
scoreboard players set #flurryCoef tmp 40
#   뇌명: 과부하·감전·초전도 피해 증가% / 줄어드는 스킬 재사용 대기(틱) / 내부 쿨타임(틱)
scoreboard players set #thunderDmg tmp 30
scoreboard players set #thunderCut tmp 20
scoreboard players set #thunderIcd tmp 16
#   반석: 결정 방어막량 증가% / 원소 피해 증가% / 지속(틱)
scoreboard players set #petraShield tmp 30
scoreboard players set #petraDmg tmp 25
scoreboard players set #petraDur tmp 200
#   광전사: 주는 피해 증가% / 받는 피해 증가% / 처치 후 공격 속도 증가 / 지속(틱)
scoreboard players set #berDmg tmp 25
scoreboard players set #berTaken tmp 20
scoreboard players set #berSpd tmp 30
scoreboard players set #berT tmp 60
# 아이템 수치 (설명 글은 각 아이템 def 에 따로 적혀 있으니 같이 고칠 것. 피해 계수는 items/proc/* 의 dmg_calc)
# #hourglassCd: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b2)
scoreboard players set #hourglassCd tmp 50
scoreboard players set #slatePct tmp 30
scoreboard players set #pouchGold tmp 1
scoreboard players set #herbPct tmp 50
scoreboard players set #hoodHp tmp 50
scoreboard players set #hoodDmg tmp 10
scoreboard players set #rainDur tmp 240
scoreboard players set #rainCdT tmp 20
scoreboard players set #ravenDur tmp 200
scoreboard players set #potN tmp 4
scoreboard players set #potGap tmp 25
scoreboard players set #flagDur tmp 160
scoreboard players set #flagAtk tmp 20
# #flagHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b4)
scoreboard players set #flagHeal tmp 20
scoreboard players set #mapleDur tmp 160
scoreboard players set #mapleDmg tmp 25
scoreboard players set #mapleCdT tmp 280
scoreboard players set #jadePct tmp 30
scoreboard players set #jadeDur tmp 400
scoreboard players set #quillN tmp 6
scoreboard players set #quillDur tmp 200
scoreboard players set #bunnyDur tmp 100
scoreboard players set #bunnyCdT tmp 300
scoreboard players set #talDur tmp 160
# #talHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b8)
scoreboard players set #talHeal tmp 20
scoreboard players set #talCdT tmp 10
scoreboard players set #blossomDur tmp 400
scoreboard players set #blossomCdT tmp 40
# #huntPer: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b5)
scoreboard players set #huntPer tmp 30
scoreboard players set #huntMax tmp 10
scoreboard players set #thiefGold tmp 1
scoreboard players set #thiefCdT tmp 20
scoreboard players set #quillHit itv 0
scoreboard players set #blossomHit itv 0
scoreboard players set #basic itv 0
# 아이템 수치 2차 (설명 글은 각 아이템 def 에 따로 적혀 있으니 같이 고칠 것. 피해 계수는 items/proc/* 의 dmg_calc · calc_stat)
scoreboard players set #jellyDur tmp 240
# #jellyHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b7)
scoreboard players set #jellyHeal tmp 20
scoreboard players set #gflagDur tmp 200
scoreboard players set #gflagDef tmp 25
scoreboard players set #gflagDmg tmp 15
scoreboard players set #skDur tmp 400
scoreboard players set #skCdT tmp 30
scoreboard players set #mirShield tmp 12
scoreboard players set #mirDmg tmp 18
scoreboard players set #mirDur tmp 160
scoreboard players set #ringDur tmp 240
scoreboard players set #dollDur tmp 300
scoreboard players set #chalMax tmp 4
scoreboard players set #chalEm tmp 60
scoreboard players set #chalDur tmp 160
scoreboard players set #wispFuse tmp 30
scoreboard players set #wispCdT tmp 80
scoreboard players set #houndDur tmp 200
# #houndHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b5)
scoreboard players set #houndHeal tmp 10
scoreboard players set #gringCost tmp 20
scoreboard players set #gringDur tmp 240
# #gringHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b4)
scoreboard players set #gringHeal tmp 20
scoreboard players set #vortexDur tmp 40
scoreboard players set #muskAtk tmp 20
scoreboard players set #muskDur tmp 160
scoreboard players set #salonDur tmp 400
scoreboard players set #salonCost tmp 2
scoreboard players set #salonDmg tmp 40
scoreboard players set #sakDur tmp 800
scoreboard players set #srcDur tmp 200
scoreboard players set #srcDmg tmp 35
scoreboard players set #oathMax tmp 50
scoreboard players set #oathBasic tmp 10
scoreboard players set #oathDur tmp 200
scoreboard players set #st30 tmp 30
scoreboard players set #st40 tmp 40
scoreboard players set #st60 tmp 60
scoreboard players set #sub itv 0
# 각인 수치 2차 (설명 글은 engravings/register)
#   해류·금강: 더해지는 피해 = 최대 체력 / 방어력 × N ÷ 1000
scoreboard players set #es_tide2 tmp 15
scoreboard players set #es_vajra2 tmp 12
scoreboard players set #es_erode2 tmp 80
scoreboard players set #tidePm tmp 30
scoreboard players set #vajraPm tmp 200
#   연계: 스킬·폭발 피해 증가% / 기본 공격 피해 증가% / 지속(틱)
scoreboard players set #chainSkill tmp 15
scoreboard players set #chainBasic tmp 30
scoreboard players set #chainDur tmp 120
#   침식: 받는 피해 증가% / 지속(틱)
scoreboard players set #erodeDmg tmp 20
scoreboard players set #erodeDur tmp 160
#   월광: 격변 반응 피해 증가%
scoreboard players set #lunarDmg tmp 20
#   협동: 아이템 효과 피해 증가% / 공격력 증가% / 지속(틱)
scoreboard players set #coopDmg tmp 25
scoreboard players set #coopAtk tmp 15
scoreboard players set #coopDur tmp 100
#   전의: 원소폭발 피해 증가% / 공격력 증가% / 지속(틱)
scoreboard players set #spiritBurst tmp 20
scoreboard players set #spiritAtk tmp 25
scoreboard players set #spiritDur tmp 200
# 아이템 수치 3차 (mythic · 신규 unique · 신규 rare)
scoreboard players set #stormDur tmp 120
scoreboard players set #stormEnergy tmp 2500
scoreboard players set #jadeRes tmp 20
scoreboard players set #mayaDur tmp 300
scoreboard players set #mayaEm tmp 200
scoreboard players set #fanDur tmp 360
scoreboard players set #fanGain tmp 400
scoreboard players set #fanMax tmp 100
scoreboard players set #oathBurst tmp 2
scoreboard players set #moonCdT tmp 40
scoreboard players set #omenDur tmp 160
scoreboard players set #omenDmg tmp 20
scoreboard players set #caseDur tmp 400
scoreboard players set #seamDur tmp 280
# #seamShield: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b8)
scoreboard players set #seamShield tmp 60
# #seamHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b8)
scoreboard players set #seamHeal tmp 20
scoreboard players set #dragDur tmp 240
scoreboard players set #dragRx tmp 25
scoreboard players set #dragFire tmp 15
scoreboard players set #tenguDur tmp 120
scoreboard players set #tenguAtk tmp 15
scoreboard players set #operaDur tmp 240
scoreboard players set #operaMax tmp 20
scoreboard players set #operaPm tmp 300
# #barAdd: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b4)
scoreboard players set #barAdd tmp 20
scoreboard players set #barCap tmp 12
scoreboard players set #barCdT tmp 10
# #nightShield: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b5)
scoreboard players set #nightShield tmp 80
scoreboard players set #nightDur tmp 240
scoreboard players set #genieDur tmp 200
scoreboard players set #genieEnergy tmp 400
# #genieHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b4)
scoreboard players set #genieHeal tmp 20
scoreboard players set #kinDur tmp 100
scoreboard players set #kinAtk tmp 15
scoreboard players set #orbCdT tmp 60
scoreboard players set #slimeDur tmp 160
scoreboard players set #slimeEm tmp 80
scoreboard players set #st50 tmp 50
scoreboard players set #neg1 tmp -1
# 아이템 수치 4차 (설명 글은 각 아이템 def 에 따로 적혀 있으니 같이 고칠 것. 피해 계수·회복 계수는 items/proc/*)
scoreboard players set #beadsHeal tmp 15
scoreboard players set #thimbleDmg tmp 8
# #bracerRes: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b1)
scoreboard players set #bracerRes tmp 60
scoreboard players set #inkBol tmp 15
scoreboard players set #maidCdT tmp 40
scoreboard players set #cocktailSpd tmp 10
scoreboard players set #sinDur tmp 200
scoreboard players set #sinCrit tmp 12
scoreboard players set #daggerSpd tmp 15
scoreboard players set #candDur tmp 200
scoreboard players set #candDmg tmp 20
scoreboard players set #dandDur tmp 160
scoreboard players set #dandSpd tmp 15
scoreboard players set #craneDur tmp 80
scoreboard players set #nurseBol tmp 20
scoreboard players set #nurseEnergy tmp 600
scoreboard players set #harmDur tmp 120
scoreboard players set #harmDmg tmp 10
scoreboard players set #pillowDur tmp 120
scoreboard players set #pillowEm tmp 80
scoreboard players set #pillowSpd tmp 10
scoreboard players set #loomDur tmp 160
scoreboard players set #loomEm tmp 150
scoreboard players set #mechCdT tmp 60
# #gourdHeal: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b9)
scoreboard players set #gourdHeal tmp 20
scoreboard players set #gourdDmg tmp 15
# #lionRes: 천분율(‰) 단위 (아이템 강화 배율에서 값이 고르게 바뀌도록. 조정 표 = items/tune/b1)
scoreboard players set #lionRes tmp 150
scoreboard players set #lionCdT tmp 40
scoreboard players set #cmoonMax tmp 45
scoreboard players set #lilyDur tmp 240
scoreboard players set #lilyCdT tmp 20
# 레벨 업 아이템 선택: 선택지 수(1~5) / 리롤 비용이 한 번마다 오르는 폭(골드. 첫 리롤은 무료) · 상한 / 선택지 하나가 신화 등급일 확률(%)
scoreboard players set #pkChoices tmp 3
# 레벨 업 선택지 한 칸이 캐릭터일 확률(%). 한 번의 선택지 묶음에 캐릭터는 최대 하나, 지금 캐릭터는 나오지 않는다
scoreboard players set #pkCharPct tmp 8
# 레벨 업 아이템 선택의 리롤: 첫 번째 무료, 그 뒤로 주사위 #pkRerollDice 개씩 (#pkRerollStep/#pkRerollMax 는 예전 골드 비용, 지금은 안 씀)
scoreboard players set #pkRerollDice tmp 1
scoreboard players set #pkRerollStep tmp 50
scoreboard players set #pkRerollMax tmp 200
# 방 시스템: 돈 구역 골드(× 챕터) / 사파이어 구역 개수
scoreboard players set #roomGold tmp 100
scoreboard players set #roomSapphire tmp 2
# 노드: 선택지에 노드가 2개 붙을 확률(%), 주사위 구역에서 얻는 주사위 수, 생명력 구역의 최대 체력 %, 보유 칸 구역에서 늘어나는 칸 수
scoreboard players set #node2Pct tmp 25
scoreboard players set #diceGain tmp 2
scoreboard players set #hpNodePct tmp 10
scoreboard players set #slotGain tmp 2

# 원소 반응: 격변 반응의 기준 피해 = 공격력 × #reactBase%
scoreboard players set #reactBase tmp 50
# 플레이어가 맞는 원소 반응의 기준 = 받은 피해 × #rxPlayerPct%
scoreboard players set #rxPlayerPct tmp 50

# 상수
scoreboard players set #1000 tmp 1000
scoreboard players set #500 tmp 500
scoreboard players set #100 tmp 100
scoreboard players set #31 tmp 31
scoreboard players set #neg1 tmp -1
scoreboard players set #c41 tmp 41
scoreboard players set #c40 tmp 40
scoreboard players set #c65 tmp 65
scoreboard players set #c24 tmp 24
scoreboard players set #c5 tmp 5
scoreboard players set #c9 tmp 9
scoreboard players set #hb80 tmp 160
scoreboard players set #st2 tmp 2
scoreboard players set #st3 tmp 3
scoreboard players set #st4 tmp 4
scoreboard players set #st6 tmp 6
scoreboard players set #st8 tmp 8
scoreboard players set #st10 tmp 10
scoreboard players set #st15 tmp 15
scoreboard players set #st16 tmp 16
scoreboard players set #st20 tmp 20
scoreboard players set #st48 tmp 48
scoreboard players set #st150 tmp 150

# 보유 아이템 목록(획득순, 최대 invCap). 최초만 초기화
execute unless data storage rlk:pinv order run data modify storage rlk:pinv order set value []
execute unless data storage rlk:pinv enh run data modify storage rlk:pinv enh set value {}

function rlk:element/setup
function rlk:char/setup
function rlk:player/hud/setup
function rlk:engravings/register
scoreboard players set #abyssHit tmp 0
execute unless score #abStack eng matches 0.. run scoreboard players set #abStack eng 0
execute unless score #aqN eng matches 0.. run scoreboard players set #aqN eng 0
scoreboard players set @a[tag=player] invDirty 2
# 시점 시스템: F5 위쪽 시점 하나(1인칭 · 숄더뷰는 11-10 에 없앰; 개발자 모드만 아바타 없이 view/fps_tick). #on view 1 · #vmode view 2 는
# 고정값으로 남긴다(읽는 곳: 생성된 mboss/guardian/p/pull/scr_end). 1인칭(#on 0) · 숄더뷰(#vmode 1)로 저장된 월드도 여기서 F5 가 되고,
# 아바타 · 받침은 다음 틱의 view/fresh → view/tick 이 새로 만든다
scoreboard players set #on view 1
scoreboard players set #vmode view 2
# 서버 시작·/reload 뒤 첫 틱에 시점 엔티티를 새로 만든다(view/fresh)
scoreboard players set #vFresh view 1
# F5 위쪽 시점: 카메라 거리(칸) · 받침 크기(1 = 머리 위 약 1칸, 0.5 = 0.5칸, 1.5 = 1.5칸)
execute unless data storage rlk:view ride run data modify storage rlk:view ride set value {d:3.5d,s:0.5d}
# 카메라 거리·높이 기본을 한 칸씩 당긴 판(ridev 2): 한 번만 '보통'으로 맞춤
execute unless data storage rlk:view {ridev:2} run data modify storage rlk:lobby cfg set value {dist:1,side:0,h:1}
execute unless data storage rlk:view {ridev:2} run data modify storage rlk:view ride set value {d:3.5d,s:0.5d}
data modify storage rlk:view ridev set value 2
execute unless score #avId view matches 0.. run scoreboard players set #avId view 0
# 없앤 숄더뷰 카메라의 저장값(위치 · 따라오기 · 작업 칸)
data remove storage rlk:view cam
data remove storage rlk:view opt
data remove storage rlk:view optv
data remove storage rlk:view st
data remove storage rlk:view pr
execute unless score #spr view matches 0..1 run scoreboard players set #spr view 0
function rlk:view/rays
team add rlk_cam
team modify rlk_cam seeFriendlyInvisibles false
# 경직용 팀: 몸(1인칭의 플레이어 / 숄더뷰의 아바타)이 들어 있고, 경직 중인 몹이 잠깐 들어온다
team add rlk_stun
team modify rlk_stun seeFriendlyInvisibles false
kill @e[tag=rlk_view]
function rlk:items/register
function rlk:engravings/byeng_build
# 아이템 너프 · 강화 배율(상수 기준값 잡기 + 강화 단계 반영 + 설명 숫자)
function rlk:items/tune/register
function rlk:char/reg_items
# 아이템 선택 공간(검은 방)이 있는 청크는 항상 불러와 둔다
execute in minecraft:overworld run forceload add 104 4
# 중간보스 원형 경기장(중심 200 201 8, 청크 9개)도 항상 불러와 둔다: 몸체 소환 · 정리가 같은 틱에 되어야 함
execute in minecraft:overworld run forceload add 176 -16 223 31
execute unless data storage rlk:lvpick choices run data modify storage rlk:lvpick choices set value []
kill @e[tag=rlk_pk]
scoreboard players set @a[scores={pkMode=1..}] pkRedraw 2
# 아이템 설명 판 번호 +1 → 들고 있는 아이템이 새 설명으로 다시 만들어짐
execute store result score #iver tmp run data get storage rlk:items ver
scoreboard players add #iver tmp 1
execute store result storage rlk:items ver int 1 run scoreboard players get #iver tmp
function rlk:shop/register
function rlk:room/data
function rlk:room/node/register
execute unless score #active room matches 0.. run scoreboard players set #active room 0
execute unless score #combat room matches 0.. run scoreboard players set #combat room 0
execute unless score #setup room matches 0.. run scoreboard players set #setup room 0
execute unless score #ogid room matches 0.. run scoreboard players set #ogid room 0
execute unless data storage rlk:room ready run data modify storage rlk:room ready set value 0b
# 던전 구역 위치가 바뀐 버전이면 다시 준비해야 함
execute unless data storage rlk:room {area:"s0"} run data modify storage rlk:room ready set value 0b

# 접속 중인 플레이어 초기화
execute as @a[tag=player] unless score @s init matches 1 run function rlk:player/init
execute as @a[tag=player] unless score @s level matches 1.. run function rlk:player/init
# 전투 개편 C 전에 저장된 플레이어: 패링 · 닷지 시각 도장(대쉬 충전은 없어짐)
execute as @a[tag=player] unless score @s parHit matches -2147483648.. run function rlk:player/def/reset
# 이미 초기화된 플레이어(업데이트 전 월드)도 보유 칸 수가 있게
execute as @a[tag=player] unless score @s invCap matches 9..18 run scoreboard players set @s invCap 9

# 리로드 시 재생성: 클릭 감지 인터랙션 / 체력바 / 몹 실드
kill @e[type=minecraft:interaction,tag=atkBlock]
kill @e[type=minecraft:interaction,tag=atkStrike]
tag @e remove rlk_mob
kill @e[tag=rlk_hb_bg]
kill @e[tag=rlk_hb_fg]
kill @e[tag=rlk_hb_num]
kill @e[tag=rlk_hb_lv]
kill @e[tag=rlk_hb_er]
kill @e[tag=rlk_hb_icon]
kill @e[tag=rlk_mshield]
# 악요의 눈 조각은 리로드 때 새로 만든다(모양이 바뀌었을 수 있음)
kill @e[tag=rlk_eye]
kill @e[tag=rlk_frz_ice]
scoreboard players set @e icKey -1
# 드롭 아이템 정리
kill @e[tag=rlk_ditem]
kill @e[tag=rlk_dinfo]
kill @e[tag=rlk_dbtn]
kill @e[tag=rlk_dlbl]
data modify storage rlk:ditems records set value {}

tellraw @a [{"text":"[로그라이크] 시스템 로드 완료","color":"green"},{"text":" · 빌드 11-06 홍련 · 특수 보스","color":"gray"}]
# 리로드 시 전원 강제 재스캔(새 objective/아이템 플래그 즉시 반영)
execute as @a[tag=player] if score @s init matches 1 run function rlk:items/equip_scan
scoreboard players set @a[tag=player] invDirty 2
scoreboard players set #naD tmp 100
# 예전 이름의 표시 지우기
scoreboard players reset 밤의순찰 stacks
# 네페르 그림자를 치우는 곳(죽는 모습이 안 보이게)
forceload add 1000000 1000000
team add rlk_nfshade
team modify rlk_nfshade color dark_green
team modify rlk_nfshade collisionRule never
# 퍼펙트 닷지의 붉은 잔상(빛나는 테두리 색, player/def/fx/pd_ghost)
team add rlk_cbred
team modify rlk_cbred color red
team modify rlk_cbred collisionRule never
team modify rlk_cbred seeFriendlyInvisibles false
# ===== 1챕터 커스텀 몹(cm) =====
scoreboard players set #15 tmp 15
scoreboard players set #6 tmp 6
scoreboard players set #5000 tmp 5000
scoreboard players set #25 tmp 25
scoreboard players set #5 tmp 5
scoreboard players set #4 tmp 4
# 피해(원피해, 1레벨 기준 — 몹 레벨 보정은 player/take_damage). 기존 허스크 근접 = 15
scoreboard players set #cmD_sw tmp 15
scoreboard players set #cmD_ar tmp 14
scoreboard players set #cmD_fb tmp 8
scoreboard players set #cmD_icD tmp 12
scoreboard players set #cmD_icB tmp 8
scoreboard players set #cmD_shS tmp 15
scoreboard players set #cmD_shR tmp 20
scoreboard players set #cmD_cn tmp 22
# 공격 간격(틱)
scoreboard players set #cmCd_sw tmp 30
scoreboard players set #cmCd_ar tmp 50
scoreboard players set #cmCd_fm tmp 80
scoreboard players set #cmCd_im tmp 90
scoreboard players set #cmCd_sh tmp 35
scoreboard players set #cmCd2_sh tmp 140
scoreboard players set #cmCd_cn tmp 90
# 선딜(틱): 검사 베기 · 궁수 차지(마지막 #cmW_arL 틱은 조준 고정) · 불 마법사 차지/발사 간격 · 얼음 마법사 차지/고드름 매달림 · 방패병 휘두르기/돌진 준비/돌진 끝 휘두르기 · 대포 심지
scoreboard players set #cmW_sw tmp 12
scoreboard players set #cmW_ar tmp 36
scoreboard players set #cmW_arL tmp 10
scoreboard players set #cmW_fm tmp 40
scoreboard players set #cmW_fmG tmp 10
scoreboard players set #cmW_im tmp 30
scoreboard players set #cmW_imH tmp 24
scoreboard players set #cmW_sh tmp 16
scoreboard players set #cmW_shR tmp 26
scoreboard players set #cmW_shE tmp 8
scoreboard players set #cmW_cn tmp 36
# 대포: 조준(표시) 뒤 발사까지
scoreboard players set #cmW_cnD tmp 16
# 방패 내구도 = 최대 체력의 #cmShPct %, 방패병이 도는 속도(0.01°/틱)
scoreboard players set #cmShPct tmp 70
scoreboard players set #cmTurn tmp 600
scoreboard players set #cmTurnN tmp -600
scoreboard players set #m1 tmp -1
scoreboard players set #3 tmp 3
scoreboard players set #35 tmp 35
team add rlk_cmx
team modify rlk_cmx collisionRule never
function rlk:cm/c2/load
function rlk:cm/c3/load

# 지도 클릭 화면 (2026-10-10)
scoreboard objectives add vMapL dummy
scoreboard objectives add vMapR dummy
scoreboard players set #128 view 128
execute as @a[tag=player,scores={vMap=1}] run function rlk:view/map_close

# 검사 디스플레이 모션: 상태/피격/회복/이동/자세/사망 시간
scoreboard objectives add cmAF dummy
scoreboard objectives add cmAH dummy
scoreboard objectives add cmAR dummy
scoreboard objectives add cmAX dummy
scoreboard objectives add cmAZ dummy
scoreboard objectives add cmAP dummy
scoreboard objectives add cmAD dummy
execute as @e[tag=rlk_cmb,tag=rlk_cm_sw] at @s run function rlk:cm/sw/rig/rebuild

execute as @e[tag=rlk_cmb,tag=rlk_cm_ar] at @s run function rlk:cm/ar/rig/rebuild

execute as @e[tag=rlk_cmb,tag=rlk_cm_fm] at @s run function rlk:cm/fm/rig/rebuild

execute as @e[tag=rlk_cmb,tag=rlk_cm_im] at @s run function rlk:cm/im/rig/rebuild

execute as @e[tag=rlk_cmb,tag=rlk_cm_sh] at @s run function rlk:cm/sh/rig/rebuild

execute as @e[tag=rlk_cmb,tag=rlk_cm_cn] at @s run function rlk:cm/cn/rig/rebuild

# 리로드 중 남은 짧은 피격 이동/방향 표식 정리
kill @e[tag=rlk_plkb]
kill @e[tag=rlk_plkb_source]
kill @e[tag=rlk_melee_origin]

function rlk:char/motion/install

# 리소스팩 보스바(tools/build_bossbar.py)
function rlk:bossui/init
# Narukami encounter and rig, rebuilt without refilling an existing boss.
function rlk:boss/raiden/init
# 중간보스 틀(tools/build_mboss_core.py): 점수 · 보스바 · 레지스트리 · 경기장 확인, 진행 중 전투는 체력 유지
function rlk:mboss/init
# rift (build_rift.py)
function rlk:room/rift/init
# 균형치 · 그로기(tools/build_balance.py): 점수 · 조절값 · 마름모 줄 표
function rlk:bal/load
# 화면 위 미니맵(tools/build_minimap.py)
function rlk:minimap/init
# 나비아 금빛 카드 효과 점수(tools/build_navia_fx_cards.py)
function rlk:fx/nv/init
