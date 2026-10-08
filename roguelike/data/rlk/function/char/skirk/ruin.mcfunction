# 극악기 · 진 (일곱빛 섬광 중, @s = 플레이어, at 몸): 뱀의 계략을 쓰지 않는다. 주변 허계 균열을 흡수하고 고갈을 얻는다
#   고갈: 일곱빛 섬광이 끝날 때까지 일반 공격 10번의 피해 +8% (흡수한 균열 1개당 +4%, 최대 +20%)
scoreboard players operation @s burstCd = #burstCdT tmp
function rlk:char/skirk/absorb
execute if score #skAbs tmp matches 4.. run scoreboard players set #skAbs tmp 3
scoreboard players operation @s skDepB = #skAbs tmp
scoreboard players operation @s skDepB *= #c4 tmp
scoreboard players add @s skDepB 8
scoreboard players set @s skDep 10
scoreboard players set @s skDepCd 0
scoreboard players set @s buShown -1
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
playsound minecraft:block.respawn_anchor.set_spawn master @a ~ ~ ~ 0.8 1.6
playsound minecraft:block.beacon.power_select master @a ~ ~ ~ 0.6 1.9
particle minecraft:reverse_portal ~ ~1 ~ 0.5 0.7 0.5 0.3 60
particle minecraft:end_rod ~ ~1 ~ 0.5 0.7 0.5 0.08 20
function rlk:items/hook/on_cast_burst
function rlk:combat/on_skill
