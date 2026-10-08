# 게임 중 캐릭터 교체 (@s = 플레이어, macro: id). char/select 와 같지만 원소 에너지는 그대로 가져간다(재사용 대기는 0부터). 스커크가 끼면(뱀의 계략) 0부터
scoreboard players operation #keepEn tmp = @s energy
execute if score #charN tmp matches 3 run scoreboard players set #keepEn tmp 0
$function rlk:char/select {id:"$(id)"}
scoreboard players operation @s energy = #keepEn tmp
execute if score #charN tmp matches 3 run scoreboard players set @s energy 0
