# 아이템: 생명의 계약 해소 (@s = 플레이어)
# 간호사의 주사기: 해소되면 에너지·회복(다음 틱에)
execute if score @s it_nurse_syringe matches 1.. run scoreboard players set #nurseQ itv 1
