# 시점 시스템이 꺼져 있음 (@s = 플레이어): 몸 = 플레이어 자신. 아바타가 남아 있으면 정리
execute if entity @e[tag=rlk_view,limit=1] run function rlk:view/teardown
tag @s add rlk_body
# 1인칭: 플레이어가 경직용 팀에 들어 있게
execute unless entity @s[team=rlk_stun] run team join rlk_stun @s
