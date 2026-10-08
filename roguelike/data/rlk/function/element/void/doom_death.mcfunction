# 사형 선고를 받은 적이 죽음 (@s = 몹): 다음 틱에 근처 6칸 적에게 잠식의 절반을 옮긴다(char/ronova/doom_spread)
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_rndm","rlk_rndm_new"]}
scoreboard players operation @e[tag=rlk_rndm_new] rnEr = @s rnEr
scoreboard players operation @e[tag=rlk_rndm_new] rnEr /= #st2 tmp
tag @e[tag=rlk_rndm_new] remove rlk_rndm_new
tag @s remove rlk_rndoom
