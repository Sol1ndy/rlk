# 피격 (@s = 플레이어, at @s anchored eyes). 입력: #dmgIn = 원피해
# 실제 피해 = 원피해 × K / (K + 방어력), K = #defK + #defKLv × (때린 몹 레벨 - 1)
scoreboard players set #dodged tmp 0
# 대쉬 무적
execute if score @s dashInvT matches 1.. run function rlk:player/dash_iframe
execute if score #dodged tmp matches 1 run return 0
# 때린 몹의 레벨: 원피해 × (100 + #mobLvAtk·x + #mobLvAtk2·x²/100)%, x = 레벨 - 1
execute if score @s hurtLv matches 2.. run function rlk:player/hurt_lv
scoreboard players operation #dfK tmp = #defK tmp
execute if score @s hurtLv matches 2.. run function rlk:player/hurt_k
scoreboard players operation #dfD tmp = #dfK tmp
scoreboard players operation #dfD tmp += @s def
scoreboard players operation #dmgIn tmp *= #dfK tmp
scoreboard players operation #dmgIn tmp /= #dfD tmp
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
# 맞은 원소(때린 몹의 el_* 태그). 물리면 초전도 보정, 원소면 부착/반응
scoreboard players operation #elem tmp = @s hurtElem
execute unless score #elem tmp matches 0..7 run scoreboard players set #elem tmp 0
execute if score #elem tmp matches 0 if score @s scT matches 1.. run scoreboard players set #c tmp 140
execute if score #elem tmp matches 0 if score @s scT matches 1.. run scoreboard players operation #dmgIn tmp *= #c tmp
execute if score #elem tmp matches 0 if score @s scT matches 1.. run scoreboard players operation #dmgIn tmp /= #100 tmp
execute if score #elem tmp matches 1.. unless score #mbNRNow mb matches 1 run function rlk:element/player_hit
# (받는 피해 감소 등 피격 보정은 여기에 추가)
function rlk:items/proc/taken
# 각인 광전사 4개: 받는 피해 증가
execute if score berserk engN matches 4.. run function rlk:engravings/berserk/taken
# 방어막(결정)
# 각인 수호: 보호막
function rlk:engravings/guard/absorb
function rlk:element/shield_absorb
scoreboard players operation @s curHealth -= #dmgIn tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 0
scoreboard players operation #hurtDmg tmp = #dmgIn tmp
execute if score #hurtDmg tmp matches 1.. run function rlk:player/hurt_do
# (피격 시 발동 효과는 여기에 추가)
# 불사자의 갈기: 맞으면 다음 틱에 화염 반격
execute if score @s it_lion_mane matches 1.. if score #hurtDmg tmp matches 1.. unless score #lionCd itv matches 1.. run function rlk:items/proc/lion_queue
