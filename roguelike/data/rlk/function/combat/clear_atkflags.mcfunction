# 공격 플래그 초기화 (기본공격 외 경로에서 combat/apply 호출 전에 실행). 이후 필요한 값만 다시 설정
scoreboard players set #skillDmg tmp 0
scoreboard players set #elem tmp 0
scoreboard players set #elU tmp 0
scoreboard players set #icd tmp 0
scoreboard players set #tfm tmp 0
# 달 피해 표시(1 = 달빛 숫자)
scoreboard players set #lunar tmp 0
# 로노바: 이번 공허 공격의 잠식(0 = 기본 #rnErHit)
scoreboard players set #rnErAdd tmp 0
# 아이템 효과로 주는 피해 표시(각인 협동·해류·금강이 봄). 아이템 피해 함수가 피해 계산 뒤에 1 로 세우고 끝나면 내린다
scoreboard players set #sub itv 0
# 진짜 피해(중간보스 별 파괴 등, mboss/true_hit): 원소 · 보정 · 저항 없이 그대로
scoreboard players set #trueDmg tmp 0
