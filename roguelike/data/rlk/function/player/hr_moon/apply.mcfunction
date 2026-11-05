# 월하대작 (특수 보스 홍련의 이벤트 버프, @s = 플레이어, items/hook/stat_buffs 에서 2틱마다): 최종 공격력(증폭 ampAtk, 모든 공격력%
# 뒤에 곱함) · 치명타 확률 · 이동 속도. 값 = load 의 조절 지점 #hrMoonAtk / #hrMoonCrit / #hrMoonSpd (강화와 상관없음)
scoreboard players operation @s ampAtk += #hrMoonAtk tmp
scoreboard players operation @s critChance += #hrMoonCrit tmp
scoreboard players operation @s moveSpeed += #hrMoonSpd tmp
