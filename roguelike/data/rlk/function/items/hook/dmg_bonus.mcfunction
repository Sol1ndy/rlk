# 몹이 피해를 받을 때 (@s = 몹). 아이템의 '주는 피해 증가'를 #eb eng 에 더한다(각인과 합산해 한 번에 곱함). 반응 피해(#tfm)에는 호출되지 않음
# 처형인의 두건: 체력이 #hoodHp% 이하인 적
execute if score @a[tag=player,limit=1] it_hood matches 1.. run function rlk:items/proc/hood
# 사냥꾼의 표식: 같은 적 연속 타격
execute if score @a[tag=player,limit=1] it_hunter_mark matches 1.. run function rlk:items/proc/hunt
execute store result score #now itv run time query gametime
# 흑요석 거울: 표시된 적이 받는 피해
execute if score @s mirEnd > #now itv run scoreboard players operation #eb eng += #mirDmg tmp
# 음원 샘플: 원소 피해 → 그 원소의 음원이 켜진다 (3개 이상일 때의 피해 보너스는 stat_buffs)
execute if score #elem tmp matches 1..7 if score @a[tag=player,limit=1] it_source_samples matches 1.. run function rlk:items/proc/source
# 불씨의 맹약: 원소폭발 뒤 기본 공격 피해
execute if score #basic itv matches 1 unless score #sub itv matches 1 if score #oathT itv matches 1.. run scoreboard players operation #eb eng += #oathB itv
# 옥장 방패: 방패가 남아 있는 동안 몸 주변(8칸) 적이 받는 피해
execute if score #jadeT itv matches 1.. if score @a[tag=player,limit=1] shieldHP matches 1.. if entity @e[tag=rlk_body,distance=..8] run scoreboard players operation #eb eng += #jadeRes tmp
# 살롱의 초대장: 열기 1당 주는 피해 +0.3%
execute if score #fan itv matches 1.. run function rlk:items/proc/fan_bonus
# 별의 징조: 징조가 붙은 적이 받는 피해
execute if score @s omenEnd > #now itv run scoreboard players operation #eb eng += #omenDmg tmp
# 비운 깃발: 기본 공격에 방어력의 일부를 더함
execute if score #basic itv matches 1 unless score #sub itv matches 1 if score #operaT itv matches 1.. if score #operaN itv matches 1.. if score #dmg tmp matches 1.. run function rlk:items/proc/opera_add
# 아이템(4차): 마녀의 골무(스킬·폭발) · 성스러운 방패(기본 공격) · 공상의 악보 · 장생의 호리병(체력 가득) · 붉은 달의 서약
execute if score #skillDmg tmp matches 1 if score @a[tag=player,limit=1] it_witch_thimble matches 1.. run function rlk:items/proc/thimble
execute if score #basic itv matches 1 unless score #sub itv matches 1 if score #candT itv matches 1.. run scoreboard players operation #eb eng += #candDmg tmp
execute if score #harmN itv matches 1.. run function rlk:items/proc/harm_bonus
execute if score @a[tag=player,limit=1] it_life_gourd matches 1.. as @a[tag=player,limit=1] if score @s curHealth >= @s maxHealth run scoreboard players operation #eb eng += #gourdDmg tmp
execute if score @a[tag=player,limit=1] it_crimson_moon matches 1.. if score @a[tag=player,limit=1] bol matches 1.. run function rlk:items/proc/moon_bonus
# 기계 심장: 번개 원소 피해 → 낙뢰 예약
execute if score #elem tmp matches 3 unless score #sub itv matches 1 unless score #mechCd itv matches 1.. if score @a[tag=player,limit=1] it_mech_heart matches 1.. run function rlk:items/proc/mech_queue
