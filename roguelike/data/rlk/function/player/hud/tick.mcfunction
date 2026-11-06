# 액션바 HUD (@s = 플레이어, 매 틱): HP 바 · 대쉬 충전 게이지 · 원소 에너지 · 골드
# 다른 액션바 안내가 떠 있는 동안(hudHold)은 덮어쓰지 않음
execute if score @s hudHold matches 1.. run return run scoreboard players remove @s hudHold 1
# 충전 중인 칸의 진행도 #hn (0~#hudSeg) = dashRegen × #hudSeg / #dashRegenT
scoreboard players operation #hn tmp = @s dashRegen
scoreboard players operation #hn tmp *= #hudSeg tmp
scoreboard players operation #hn tmp /= #dashRegenT tmp
execute if score #hn tmp > #hudSeg tmp run scoreboard players operation #hn tmp = #hudSeg tmp
# 모양이 바뀔 때만 게이지를 다시 조립 (키 = 충전 수 × 100 + 진행도)
scoreboard players operation #hk tmp = @s dashCharge
scoreboard players operation #hk tmp *= #100 tmp
scoreboard players operation #hk tmp += #hn tmp
execute unless score #hk tmp = @s hudKey run function rlk:player/hud/build
# HP 바의 찬 칸 수 #hpN = 올림(현재 체력 × #hudHpSeg / 최대 체력). 바뀔 때만 다시 조립
scoreboard players operation #hpN tmp = @s curHealth
scoreboard players operation #hpN tmp *= #hudHpSeg tmp
scoreboard players operation #hpN tmp += @s maxHealth
scoreboard players remove #hpN tmp 1
scoreboard players operation #hpN tmp /= @s maxHealth
execute if score #hpN tmp matches ..-1 run scoreboard players set #hpN tmp 0
execute if score #hpN tmp > #hudHpSeg tmp run scoreboard players operation #hpN tmp = #hudHpSeg tmp
execute unless score #hpN tmp = @s hpKey run function rlk:player/hud/hp_build
# 원소 에너지 게이지의 찬 칸 수 = 에너지 × 15 / 필요량. 바뀔 때만 다시 조립
scoreboard players operation #enN tmp = @s energy
scoreboard players operation #enN tmp *= #hudEnSeg tmp
scoreboard players operation #enN tmp /= #burstCost100 tmp
execute if score #enN tmp > #hudEnSeg tmp run scoreboard players operation #enN tmp = #hudEnSeg tmp
execute if score #enN tmp matches ..-1 run scoreboard players set #enN tmp 0
execute unless score #enN tmp = @s enKey run function rlk:player/hud/en_build
# ❤ [HP 바] 현재/최대 (방어막) (생명의 계약 N%) (부착 원소)   대쉬 게이지   [원소 에너지] 현재/필요   골드  주사위
execute unless score @s shieldHP matches 1.. run title @s actionbar [{"text":"❤ ","color":"#E06A5A"},{"nbt":"hp","storage":"rlk:hud","interpret":true},{"text":" "},{"score":{"name":"@s","objective":"curHealth"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"maxHealth"},"color":"gray"},{"nbt":"bol[]","storage":"rlk:hud","interpret":true,"separator":""},{"text":" "},{"nbt":"aura[]","storage":"rlk:hud","interpret":true,"separator":""},{"text":"  "},{"nbt":"line[]","storage":"rlk:hud","interpret":true,"separator":" "},{"text":"   "},{"nbt":"en","storage":"rlk:hud","interpret":true},{"text":" "},{"score":{"name":"@s","objective":"energyPt"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"#burstCost","objective":"tmp"},"color":"gray"},{"text":"   "},{"text":"◆ ","color":"#E0B255"},{"score":{"name":"@s","objective":"gold"},"color":"#E0B255"},{"text":"  ⚄ ","color":"#F2F2F2"},{"score":{"name":"@s","objective":"dice"},"color":"#F2F2F2"}]
execute if score @s shieldHP matches 1.. run title @s actionbar [{"text":"❤ ","color":"#E06A5A"},{"nbt":"hp","storage":"rlk:hud","interpret":true},{"text":" "},{"score":{"name":"@s","objective":"curHealth"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"@s","objective":"maxHealth"},"color":"gray"},{"text":" ◈","color":"#F2C14E"},{"score":{"name":"@s","objective":"shieldHP"},"color":"#F2C14E"},{"nbt":"bol[]","storage":"rlk:hud","interpret":true,"separator":""},{"text":" "},{"nbt":"aura[]","storage":"rlk:hud","interpret":true,"separator":""},{"text":"  "},{"nbt":"line[]","storage":"rlk:hud","interpret":true,"separator":" "},{"text":"   "},{"nbt":"en","storage":"rlk:hud","interpret":true},{"text":" "},{"score":{"name":"@s","objective":"energyPt"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"#burstCost","objective":"tmp"},"color":"gray"},{"text":"   "},{"text":"◆ ","color":"#E0B255"},{"score":{"name":"@s","objective":"gold"},"color":"#E0B255"},{"text":"  ⚄ ","color":"#F2F2F2"},{"score":{"name":"@s","objective":"dice"},"color":"#F2F2F2"}]
