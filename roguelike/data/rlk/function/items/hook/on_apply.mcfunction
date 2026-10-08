# 몹이 데미지를 받을 때마다 (@s = 몹, at @s). #dmg 를 고치면 대상 기준 데미지 보정
# 금단의 도서: 스킬 데미지 시 마도서 페이지 획득(동일 대상 최대 3장)
execute if score #skillDmg tmp matches 1 unless score @s fbMark matches 3.. run function rlk:items/proc/forb_page
# 초월 · 악요개안: 캐릭터가 피해를 주면 그 적의 위치에 협동 공격 예약(쿨타임 1초). 반응 피해(#tfm)로는 발동하지 않음
execute unless score #tfm tmp matches 1 if score #dmg tmp matches 1.. as @a[tag=player,limit=1] if score @s it_stormy_eye matches 1.. unless score @s eyeCd matches 1.. run function rlk:items/proc/eye_queue
# 페보니우스 비전: 치명타로 피해를 주면 확률로 원소 에너지 회복 (반응 피해 제외)
execute if score #crit tmp matches 1 unless score #tfm tmp matches 1 if score #dmg tmp matches 1.. as @a[tag=player,limit=1] if score @s it_favonius_codex matches 1.. unless score @s favCd matches 1.. run function rlk:items/proc/favonius
# 도둑의 장갑: 치명타로 피해를 주면 골드
execute if score #crit tmp matches 1 unless score #tfm tmp matches 1 if score #dmg tmp matches 1.. if score @a[tag=player,limit=1] it_thief_gloves matches 1.. unless score #thiefCd itv matches 1.. run function rlk:items/proc/thief
# 치유의 부적: 스킬에 맞은 적에게 부적 / 부적이 붙은 적을 기본 공격으로 때리면 회복
execute if score @a[tag=player,limit=1] it_talisman matches 1.. unless score #tfm tmp matches 1 run function rlk:items/proc/talisman
# 얼음 깃촉: 얼음 원소 피해를 줄 때마다 깃 1개로 추가 피해(예약)
execute if score #quill itv matches 1.. if score #elem tmp matches 4 if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 unless score #quillHit itv matches 1 run function rlk:items/proc/quill_use
# 양화: 꽃 주변의 적에게 피해를 주면 바위 원소 추가 피해(예약)
execute if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 unless score #blossomHit itv matches 1 unless score #blossomCd itv matches 1.. if entity @e[tag=rlk_blossom,distance=..6,limit=1] run function rlk:items/proc/blossom_queue
# 스칸다의 씨앗: 스킬·폭발 피해 → 씨앗
execute if score #skillDmg tmp matches 1 if score @a[tag=player,limit=1] it_skandha_seed matches 1.. run function rlk:items/proc/skandha_mark
# 불씨의 맹약: 피해를 줄 때마다 전의
execute if score #dmg tmp matches 1.. unless score #tfm tmp matches 1 if score @a[tag=player,limit=1] it_ember_oath matches 1.. if score #oath itv < #oathMax tmp run scoreboard players add #oath itv 1
# 별의 징조: 스킬·폭발 피해 → 징조
execute if score #skillDmg tmp matches 1 if score @a[tag=player,limit=1] it_astral_omen matches 1.. run function rlk:items/proc/omen_mark
# 불꽃 방벽: 기본 공격 적중 → 보호막
execute if score #basic itv matches 1 unless score #sub itv matches 1 if score @a[tag=player,limit=1] it_blazing_barrier matches 1.. unless score #barCd itv matches 1.. as @a[tag=player,limit=1] run function rlk:items/proc/barrier
