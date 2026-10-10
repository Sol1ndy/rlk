# 밤 순찰 중의 일반 공격 = 권총 사격 (@s = 플레이어, at 몸). 조준 보정은 활과 같다. 번개 원소(다른 원소 부여로 바뀌지 않음)
#   생명의 계약 100% 미만: 탄환 60%, 맞히면 생명의 계약 +#clShotBol%  /  100% 이상: 관통탄 85%(줄에 있는 적 모두)
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
scoreboard players operation #cd tmp = #clShotCd tmp
scoreboard players set #as tmp 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation #as tmp = @s atkSpeed
scoreboard players operation #cd tmp /= #as tmp
execute if score #cd tmp matches ..1 run scoreboard players set #cd tmp 2
scoreboard players operation @s atkCD = #cd tmp
scoreboard players set @s cboIdle 0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
function rlk:player/bol/pct
scoreboard players set #clPierce tmp 0
execute if score #bolNow tmp matches 100.. run scoreboard players set #clPierce tmp 1
scoreboard players set #coef tmp 60
execute if score #clPierce tmp matches 1 run scoreboard players set #coef tmp 85
function rlk:char/bow/calc
# 총알이 지나갈 줄: 눈높이의 표식을 조준 방향으로 두고(조준 보정) 따라가며 맞을 적을 고른다
kill @e[tag=rlk_clm]
execute positioned ~ ~1.62 ~ positioned ^ ^-0.15 ^0.3 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_clm"]}
execute positioned ~ ~1.62 ~ positioned ^ ^-0.15 ^0.3 run tp @e[tag=rlk_clm] ~ ~ ~ ~ ~
execute as @e[tag=rlk_clm,limit=1] at @s run function rlk:char/bow/assist
scoreboard players set #cs tmp 40
scoreboard players set #cStop tmp 0
execute as @e[tag=rlk_clm,limit=1] at @s run function rlk:char/clorinde/scan
kill @e[tag=rlk_clm]
function rlk:combat/clear_atkflags
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #stunHit tmp 0
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players set #basic itv 1
scoreboard players set #bowHit tmp 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #bowHit tmp 0
execute if score #hitLanded tmp matches 1 run function rlk:combat/on_hit
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
execute if score #hitLanded tmp matches 1 if score #clPierce tmp matches 0 run function rlk:char/clorinde/shot_bol
execute if score #hitLanded tmp matches 1 run function rlk:char/clorinde/pc
function rlk:items/hook/on_basic_attack
scoreboard players set #basic itv 0
execute unless score #k255 snd matches 1 run function rlk:snd/f286
execute unless score #k256 snd matches 1 run function rlk:snd/f287
execute unless score #k257 snd matches 1 run function rlk:snd/f288
execute unless score #k258 snd matches 1 run function rlk:snd/f289
