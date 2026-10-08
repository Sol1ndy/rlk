# 경직 끝 (@s = 몹): 이동 풀기 + 원래 팀으로(숄더뷰 = 플레이어와 같은 팀 rlk_cam, 1인칭 = 팀 없음)
effect clear @s minecraft:slowness
scoreboard players set @s stunT -1
team leave @s
# 숄더뷰: 플레이어와 같은 팀으로 돌아가고, 다음 틱에 아바타에게 다시 어그로(view/mob_aggro). 1인칭은 팀이 없으면 바닐라 AI 가 알아서 플레이어를 다시 노린다
execute if entity @e[tag=rlk_av,limit=1] run team join rlk_cam @s
execute if entity @e[tag=rlk_av,limit=1] run tag @s add rlk_agq
