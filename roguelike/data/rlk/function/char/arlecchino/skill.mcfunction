# 재가 된 만상 (@s = 플레이어, at 몸): 잠깐 사라졌다가(#arSkDelay 틱) 다시 나타나며 눈앞의 적들을 벤다 → char/arlecchino/skill_hit
scoreboard players operation @s arSk = #arSkDelay tmp
# 사라짐: 1인칭 = 플레이어, 숄더뷰 = 아바타(무기도 잠깐 치운다)
execute if entity @s[tag=rlk_body] run effect give @s minecraft:invisibility 1 0 true
effect give @e[tag=rlk_av,limit=1] minecraft:invisibility 1 0 true
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
# 따라붙을 대상: 조준선 우선 → 주변 8칸에서 가장 가까운 적
tag @e[tag=rlk_artg] remove rlk_artg
execute positioned ~ ~1.62 ~ positioned ^ ^ ^ run function rlk:char/arlecchino/find
execute unless entity @e[tag=rlk_artg,limit=1] run tag @e[tag=rlk_mob,distance=..8,sort=nearest,limit=1] add rlk_artg
function rlk:char/motion/start {char:"arle",clip:"skill"}
