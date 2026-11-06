# combat/apply 의 피해 보정 묶음 (@s = 몹, at @s). 진짜 피해(#trueDmg 1)는 여기를 건너뜀
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
# 몹 저항(mres, %): 원신 저항 공식. 격변 반응에도 적용
execute if score @s mres matches 1.. if score #dmg tmp matches 1.. run function rlk:combat/res
execute if score @s mres matches ..-1 if score #dmg tmp matches 1.. run function rlk:combat/res
# Apply boss armor/exhaustion before the displayed damage value is stored.
execute if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/incoming
# 중간보스별 받는 피해 보정(그로기 등)
execute if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/incoming
