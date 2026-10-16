# 피격 대상에 데미지 표시 + 타격 이펙트 후 체력 차감 (@s = 몹, at @s)
# 입력: #dmg = 데미지, #crit = 치명타(0/1), #stunHit = 경직 여부(0/1), #skillDmg = 스킬 데미지 여부(0/1)
#       #elem = 원소(0 물리 1 불 2 물 3 번개 4 얼음 5 바위 6 바람 7 풀), #elU = 부착량(1000 = 1U, 0 = 부착 안 함)
#       #icd = 1이면 부착 쿨 적용(기본공격), #tfm = 1이면 반응 피해(증폭 안 받음)
#       ※ 호출 전에 combat/clear_atkflags 로 초기화한 뒤 필요한 값만 설정할 것
# 출력: #hitLanded, #mobKilled(처치 수 누적), #killBoss(boss 태그 처치), #killMini(miniboss 태그 처치)
# Encounter objects use attack counts, before any reactions, damage procs or loot.
execute if entity @s[tag=rlk_rd_object] run return run function rlk:boss/raiden/object/on_hit
# The transformation and the hidden real body of the illusion challenge are protected.
execute if entity @s[tag=rlk_raiden,scores={rdPhase=1}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdPat=5}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdPat=15}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdBlink=1..}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdDeath=1}] run return 0
scoreboard players set #hitLanded tmp 1
scoreboard players set #cmBlk tmp 0
# 원소: 부착/반응 → #dmg 보정(증발·융해·촉진·발산·초전도), 격변 반응 예약, 반응 이름 표시
function rlk:element/on_hit
# 아이템: 대상 기준 데미지 보정/적중 효과
# 각인: 주는 피해 증가 · 빙설의 치명타
function rlk:engravings/on_apply
function rlk:items/hook/on_apply
# 캐릭터: 요이미야의 유금화광
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/on_apply
# 레벨 보정(원신의 방어 계수): 피해 × (플레이어 레벨 + 100) / ((플레이어 레벨 + 100) + (몬스터 레벨 + 100)). 격변 반응 피해(#tfm)는 방어를 무시
# 로노바: 잠식이 쌓인 보스는 받는 피해 + 잠식/2 %
execute if score @s rnEr matches 1.. if entity @s[tag=boss] run function rlk:element/void/boss_amp
execute unless score #tfm tmp matches 1 run function rlk:combat/lv_mult
# Apply boss armor/exhaustion before the displayed damage value is stored.
execute if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/incoming
# 대미지 숫자 색 = 원소 색
function rlk:element/color
execute store result storage rlk:combat dmg int 1 run scoreboard players get #dmg tmp
# 커스텀 방패병: 정면 공격은 방패 내구도가 먼저 받음(숫자는 그대로, 다 막으면 하늘색)
execute if entity @s[tag=rlk_cm_sh] if score @s cmSh matches 1.. if score #dmg tmp matches 1.. run function rlk:cm/sh/absorb
# 아를/스커크/나비아: 방패 계산 뒤 실제 체력 피해에만 둔탁한 명중음. 추가타·스킬·궁도 같은 경로.
execute if score #charN tmp matches 3 if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 unless score #sub itv matches 1 unless score #confirmedHit snd matches 1 run function rlk:combat/confirmed_hit_sound
execute if score #charN tmp matches 5 if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 unless score #sub itv matches 1 unless score #confirmedHit snd matches 1 run function rlk:combat/confirmed_hit_sound
execute if score #charN tmp matches 6 if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 unless score #sub itv matches 1 unless score #confirmedHit snd matches 1 run function rlk:combat/confirmed_hit_sound
# 겹침 방지용 랜덤 스폰 오프셋
execute store result storage rlk:combat ox float 0.1 run random value -8..8
execute store result storage rlk:combat oz float 0.1 run random value -8..8
execute store result storage rlk:combat oy float 0.1 run random value 16..26
execute unless score #lunar tmp matches 1 if score #crit tmp matches 1 run function rlk:combat/text_crit_macro with storage rlk:combat
execute unless score #lunar tmp matches 1 if score #crit tmp matches 0 run function rlk:combat/text_normal_macro with storage rlk:combat
# 달 피해: 달빛 그라데이션 숫자
execute if score #lunar tmp matches 1 run function rlk:combat/text_lunar

# 타격 임팩트
particle minecraft:crit ~ ~1 ~ 0.25 0.35 0.25 0.12 12
particle minecraft:sweep_attack ~ ~1 ~ 0 0 0 0 1
execute if score #crit tmp matches 1 run particle minecraft:enchanted_hit ~ ~1 ~ 0.4 0.5 0.4 0.25 20
# 기본공격 경직
execute if score #stunHit tmp matches 1 unless score #cmBlk tmp matches 1 run function rlk:mob/stun
# 기본 공격: 경직을 조금 길게 + 살짝 밀어냄 (아이템 효과로 들어간 피해는 제외)
execute if score #basic itv matches 1 unless score #sub itv matches 1 unless score #bowHit tmp matches 1 if score #dmg tmp matches 1.. run function rlk:mob/basic_hit
# 화살: 경직 없이 밀어내기만(보스 제외)
execute if score #bowHit tmp matches 1 if score #dmg tmp matches 1.. unless entity @s[tag=boss] if entity @e[tag=rlk_body,limit=1] run function rlk:mob/knock
# 타격감: 빨간 피격 번쩍임 (i-frame 리셋 후 damage 0) — 실제 데미지(체력 감소)가 있을 때만
execute if score #dmg tmp matches 1.. run data merge entity @s {InvulnerableTime:0s,HurtTime:0s}
execute if score #dmg tmp matches 1.. unless entity @e[tag=rlk_av,limit=1] run damage @s 0 minecraft:generic
execute if score #dmg tmp matches 1.. if entity @e[tag=rlk_av,limit=1] unless entity @s[tag=rlk_cmb] run damage @s 0 minecraft:generic by @e[tag=rlk_av,limit=1]
# 커스텀 몹: 투명한 두뇌 대신 모습(마네킹)이 번쩍
execute if score #dmg tmp matches 1.. if entity @s[tag=rlk_cmb] run function rlk:cm/flash

# 체력 차감 (몹의 체력은 스코어 mhpC — 바닐라 체력 1024 제한 없음)
execute unless score @s mhpM matches 1.. run function rlk:mob/hp_init
scoreboard players operation #mobHP tmp = @s mhpC
scoreboard players operation #mobHP tmp -= #dmg tmp
# 로노바: 체력 비율이 잠식 아래로 떨어지면 소멸(보스 제외)
execute if score #mobHP tmp matches 1.. if score @s rnEr matches 1.. unless entity @s[tag=boss] run function rlk:element/void/exec_chk
execute if score #mobHP tmp matches ..0 run scoreboard players add #mobKilled tmp 1
execute if score #mobHP tmp matches ..0 if entity @s[tag=boss] run scoreboard players set #killBoss tmp 1
execute if score #mobHP tmp matches ..0 if entity @s[tag=miniboss] run scoreboard players set #killMini tmp 1
execute if score #mobHP tmp matches ..0 run function rlk:combat/heal_orb_roll
execute if score #mobHP tmp matches ..0 run function rlk:combat/kill_xp
execute if score #mobHP tmp matches ..0 run function rlk:combat/gold_drop
execute if score #mobHP tmp matches ..0 if score #charN tmp matches 2 run function rlk:char/yoimiya/aur_move
execute if score #mobHP tmp matches ..0 if score #charN tmp matches 5 run function rlk:char/arlecchino/dir_death
execute if score #mobHP tmp matches ..0 if entity @s[tag=rlk_rndoom] run function rlk:element/void/doom_death
execute if score #mobHP tmp matches ..0 if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/death/start
execute if score #mobHP tmp matches ..0 unless entity @s[tag=rlk_raiden] run kill @s
execute if score #mobHP tmp matches 1.. run scoreboard players operation @s mhpC = #mobHP tmp
# 빙설이 이 대상에게만 만든 치명타 표시는 되돌린다(범위 공격의 다음 대상에 번지지 않게)
execute if score #frostC eng matches 1 run scoreboard players set #crit tmp 0
execute if score #frostC eng matches 1 run scoreboard players set #frostC eng 0
