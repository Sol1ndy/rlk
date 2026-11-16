# @s = 홍련의 몸체(rlk_mb_scarlet), at @s (combat/apply; 치명타도 여기서 — 이름은 시뮬레이터들이 숫자 함수를 비우는 접두사(text_normal · text_crit)를 따름; #crit tmp, storage rlk:combat dmg / col / sc1 / sc2 가 정해진 뒤).
# round W (통합, wi_progress.md; 리뷰 w T3-09: 플레이어의 피해 숫자가 그녀를 덮어 예비 동작과 칼의 궤적이 안 보임). 보통 숫자(1.35배,
# 세 자리 약 0.6칸 폭)와 치명타(1.9배, ✧✦ 장식까지 약 3칸 폭)가 그녀의 가슴 ~ 머리(1.6 ~ 2.6칸, 좌우 ±0.8칸)에서 떠올랐다: 싸움
# 카메라(그녀까지 약 7칸, FOV 90, 1080p)에서 약 50 px · 최대 약 230 px 폭. 그녀의 숫자는 2/3 크기(0.9배 · 치명타 1.2배, 바깥 ✧ 없이)로,
# 플레이어 쪽에서 본 그녀의 왼쪽 또는 오른쪽 1.1 ~ 1.5칸, 어깨 ~ 머리 높이(1.9 ~ 2.4칸)에서 떠오른다(수명 · 떠오름은 combat/text_tick 그대로)
execute store result storage rlk:combat ox float 0.1 run random value -2..2
execute store result storage rlk:combat oz float 0.1 run random value 11..15
execute store result storage rlk:combat oy float 0.1 run random value 19..24
execute store result score #dnL tmp run random value 0..1
execute if score #dnL tmp matches 1 store result storage rlk:combat oz float -0.1 run data get storage rlk:combat oz 10
execute if score #crit tmp matches 1 facing entity @a[tag=player,limit=1] feet rotated ~90 0 run function rlk:combat/text_crit_side with storage rlk:combat
execute unless score #crit tmp matches 1 facing entity @a[tag=player,limit=1] feet rotated ~90 0 run function rlk:combat/text_normal_side_n with storage rlk:combat
