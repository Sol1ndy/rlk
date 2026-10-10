# 쓰러짐이 끝난 뒤 몹을 원래 팀으로 (@s = 몹): 숄더뷰 = 플레이어와 같은 팀 rlk_cam + 다음 틱에 아바타를 노림, 1인칭 = 팀 없음(바닐라 AI 가 플레이어를 노림)
team leave @s
execute if entity @e[tag=rlk_av,limit=1] run team join rlk_cam @s
execute if entity @e[tag=rlk_av,limit=1] run tag @s add rlk_agq
