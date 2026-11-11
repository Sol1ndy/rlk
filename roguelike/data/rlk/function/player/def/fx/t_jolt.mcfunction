# 화면 튐을 되돌린다(@s = 표식, 만든 다음 틱): p3 이 준 만큼 반대로. 위아래(pitch)까지 튀었으면(rlk_cb_jp) 그것도
execute if entity @s[tag=rlk_cb_jp] as @a[tag=player,limit=1] at @s run rotate @s ~-1.5 ~1
execute unless entity @s[tag=rlk_cb_jp] as @a[tag=player,limit=1] at @s run rotate @s ~-1.5 ~
