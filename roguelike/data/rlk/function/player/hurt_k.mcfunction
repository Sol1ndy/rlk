# 방어 상수 K (@s = 플레이어): 때린 몹의 레벨이 높을수록 같은 방어력으로 덜 막음. K = #defK + #defKLv·(hurtLv - 1)
scoreboard players operation #dfX tmp = @s hurtLv
scoreboard players remove #dfX tmp 1
scoreboard players operation #dfX tmp *= #defKLv tmp
scoreboard players operation #dfK tmp += #dfX tmp
