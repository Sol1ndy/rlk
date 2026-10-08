scoreboard players set @s devMode 0
# 즉시 인벤 재정렬
scoreboard players set @s invDirty 2
tellraw @s [{"text":"[개발자 모드] ","color":"gold","bold":true},{"text":"OFF — 슬롯 고정 복구","color":"red"}]
