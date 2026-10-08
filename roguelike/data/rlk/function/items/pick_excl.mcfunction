# at = 상점 위치. cid(뽑힌 후보)를 근처(64) 플레이어 소지 기반으로 제외 → #excl
# 봉인된 검: 키리온(상위형) 또는 봉인된 검 이미 보유 시 제외
execute if data storage rlk:pick {cid:"sealed_sword"} if entity @p[distance=..64,scores={it_sword_kirion=1..}] run scoreboard players set #excl tmp 1
execute if data storage rlk:pick {cid:"sealed_sword"} if entity @p[distance=..64,scores={it_sealed_sword=1..}] run scoreboard players set #excl tmp 1
# 금단의 도서: 데모노미콘(진화 상위형) 또는 금단의 도서 이미 보유 시 제외
execute if data storage rlk:pick {cid:"forbidden_book"} if entity @p[distance=..64,scores={it_demonomicon=1..}] run scoreboard players set #excl tmp 1
execute if data storage rlk:pick {cid:"forbidden_book"} if entity @p[distance=..64,scores={it_forbidden_book=1..}] run scoreboard players set #excl tmp 1
