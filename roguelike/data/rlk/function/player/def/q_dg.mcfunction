# @s = 플레이어 (player/def/q_pf: 물은 틱이 이번 닷지의 퍼펙트 창 안). 그 닷지가 공격을 피했다: 재사용 대기 돌려받기(닷지 한 번에 한 번)
execute unless score @s dgAt = #dgRf cb run function rlk:player/def/dg_refund
return 1
