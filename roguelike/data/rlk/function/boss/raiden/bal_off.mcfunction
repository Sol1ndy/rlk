# rlk:bal/grog/end, as the boss: the balance stun ends with the gauge clock (pattern finish, the AI resumes)
execute if score @s rdPat matches 98 if score @s rdSgStun matches 4 run function rlk:boss/raiden/sg/stun_end
