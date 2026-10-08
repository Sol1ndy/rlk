# 사형 선고 (@s = 플레이어, at 몸): 조준한 적 하나에게 공격력의 220% 공허 원소 피해 + 잠식 +15%. 이 적이 죽으면 근처 6칸 적에게 잠식의 절반이 옮겨 간다
tag @e[tag=rlk_rntg] remove rlk_rntg
execute anchored eyes positioned ^ ^ ^ run function rlk:char/ronova/find
execute unless entity @e[tag=rlk_rntg,limit=1] run tag @e[tag=rlk_mob,distance=..5,sort=nearest,limit=1] add rlk_rntg
execute unless entity @e[tag=rlk_rntg,limit=1] run return run function rlk:char/deny {t:"사형을 선고할 적이 없음"}
scoreboard players operation @s skillCd = #skillCdT tmp
function rlk:char/cd_reduce
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
function rlk:char/dmg_calc {coef:220}
scoreboard players set #elem tmp 8
scoreboard players set #elU tmp 1000
scoreboard players set #rnErAdd tmp 15
tag @e[tag=rlk_rntg] add rlk_rndoom
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_rntg] at @s run function rlk:char/ronova/doom_fx
execute as @e[tag=rlk_rntg] at @s run function rlk:combat/apply_reset
execute if score #hitLanded tmp matches 1 run function rlk:char/particles {n:3,el:8}
tag @e[tag=rlk_rntg] remove rlk_rntg
function rlk:char/after_hit
playsound minecraft:entity.elder_guardian.curse master @a ~ ~ ~ 0.35 1.5
playsound minecraft:block.bell.resonate master @a ~ ~ ~ 0.5 0.6
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
