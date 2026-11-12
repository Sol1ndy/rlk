# @s = 플레이어, at 몸 eyes. 3단계(퍼펙트) 패링: 피해 무효. 이 F 의 첫 막기에서만(같은 틱의 여러 타격은 한 번): 원소전투 스킬
# 재사용 대기 -#parCut 틱(모든 캐릭터, char/cd_cut), 공격한 적의 균형치 한 칸(rlk:bal/hit {n:1}), 효과 · 소리, 아이템 신호
scoreboard players set #dodged tmp 1
scoreboard players set #parT tmp 3
execute unless score @s parHit = #now cb run function rlk:player/def/par3_go
function rlk:player/def/par_use
execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q
