# 재가 된 만상 (@s = 플레이어, at 몸): 잠깐 사라졌다가(#arSkDelay 틱) 다시 나타나며 눈앞의 적들을 벤다 → char/arlecchino/skill_hit
scoreboard players operation @s arSk = #arSkDelay tmp
# 사라짐: 1인칭 = 플레이어, 숄더뷰 = 아바타(무기도 잠깐 치운다)
execute if entity @s[tag=rlk_body] run effect give @s minecraft:invisibility 1 0 true
effect give @e[tag=rlk_av,limit=1] minecraft:invisibility 1 0 true
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 25
particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.6} ~ ~1 ~ 0.35 0.7 0.35 0 30
particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.03 15
playsound minecraft:entity.enderman.teleport master @a ~ ~ ~ 0.5 0.6
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.5 0.6
# 따라붙을 대상: 조준선 우선 → 주변 8칸에서 가장 가까운 적
tag @e[tag=rlk_artg] remove rlk_artg
execute anchored eyes positioned ^ ^ ^ run function rlk:char/arlecchino/find
execute unless entity @e[tag=rlk_artg,limit=1] run tag @e[tag=rlk_mob,distance=..8,sort=nearest,limit=1] add rlk_artg
