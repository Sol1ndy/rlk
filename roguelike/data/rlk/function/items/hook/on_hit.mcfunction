# 기본공격 적중 시 아이템 효과 (@s = 플레이어, at @s)
# 메이드의 건틀릿: 적중 시 회복
execute if score @s it_maid_gauntlet matches 1.. unless score #maidCd itv matches 1.. run function rlk:items/proc/maid
# 수련의 무희: 적중 표시(다음 틱에 물 폭발)
execute if score #lilyT itv matches 1.. unless score #lilyCd itv matches 1.. run scoreboard players set #lilyHit itv 1
