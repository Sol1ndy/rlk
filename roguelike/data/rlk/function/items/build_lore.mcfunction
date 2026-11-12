# lore 자동 생성 (storage rlk:io.src 기준)
# base 색: 인벤=gray, 드롭/상점(clickdrop 없음)=white
data modify storage rlk:io basecolor set value "gray"
execute unless data storage rlk:io clickdrop run data modify storage rlk:io basecolor set value "white"

# 1) 스탯 라인
execute if data storage rlk:io src.stats.atkPct run data modify storage rlk:io v set from storage rlk:io src.stats.atkPct
execute if data storage rlk:io src.stats.atkPct run function rlk:items/lore/atkpct with storage rlk:io
execute if data storage rlk:io src.stats.atkFlat run data modify storage rlk:io v set from storage rlk:io src.stats.atkFlat
execute if data storage rlk:io src.stats.atkFlat run function rlk:items/lore/atkflat with storage rlk:io
execute if data storage rlk:io src.stats.hpPct run data modify storage rlk:io v set from storage rlk:io src.stats.hpPct
execute if data storage rlk:io src.stats.hpPct run function rlk:items/lore/hppct with storage rlk:io
execute if data storage rlk:io src.stats.hpFlat run data modify storage rlk:io v set from storage rlk:io src.stats.hpFlat
execute if data storage rlk:io src.stats.hpFlat run function rlk:items/lore/hpflat with storage rlk:io
execute if data storage rlk:io src.stats.defPct run data modify storage rlk:io v set from storage rlk:io src.stats.defPct
execute if data storage rlk:io src.stats.defPct run function rlk:items/lore/defpct with storage rlk:io
execute if data storage rlk:io src.stats.defFlat run data modify storage rlk:io v set from storage rlk:io src.stats.defFlat
execute if data storage rlk:io src.stats.defFlat run function rlk:items/lore/defflat with storage rlk:io
execute if data storage rlk:io src.stats.elemMastery run data modify storage rlk:io v set from storage rlk:io src.stats.elemMastery
execute if data storage rlk:io src.stats.elemMastery run function rlk:items/lore/elemmastery with storage rlk:io
execute if data storage rlk:io src.stats.critChance run data modify storage rlk:io v set from storage rlk:io src.stats.critChance
execute if data storage rlk:io src.stats.critChance run function rlk:items/lore/setsign
execute if data storage rlk:io src.stats.critChance run function rlk:items/lore/critchance with storage rlk:io
execute if data storage rlk:io src.stats.critDamage run data modify storage rlk:io v set from storage rlk:io src.stats.critDamage
execute if data storage rlk:io src.stats.critDamage run function rlk:items/lore/critdamage with storage rlk:io
execute if data storage rlk:io src.stats.moveSpeed run data modify storage rlk:io v set from storage rlk:io src.stats.moveSpeed
execute if data storage rlk:io src.stats.moveSpeed run function rlk:items/lore/movespeed with storage rlk:io
execute if data storage rlk:io src.stats.atkSpeed run data modify storage rlk:io v set from storage rlk:io src.stats.atkSpeed
execute if data storage rlk:io src.stats.atkSpeed run function rlk:items/lore/atkspeed with storage rlk:io
execute if data storage rlk:io src.stats.energyRecharge run data modify storage rlk:io v set from storage rlk:io src.stats.energyRecharge
execute if data storage rlk:io src.stats.energyRecharge run function rlk:items/lore/energyrecharge with storage rlk:io
execute if data storage rlk:io src.stats.physBonus run data modify storage rlk:io v set from storage rlk:io src.stats.physBonus
execute if data storage rlk:io src.stats.physBonus run function rlk:items/lore/physbonus with storage rlk:io
execute if data storage rlk:io src.stats.pyroBonus run data modify storage rlk:io v set from storage rlk:io src.stats.pyroBonus
execute if data storage rlk:io src.stats.pyroBonus run function rlk:items/lore/pyrobonus with storage rlk:io
execute if data storage rlk:io src.stats.hydroBonus run data modify storage rlk:io v set from storage rlk:io src.stats.hydroBonus
execute if data storage rlk:io src.stats.hydroBonus run function rlk:items/lore/hydrobonus with storage rlk:io
execute if data storage rlk:io src.stats.electroBonus run data modify storage rlk:io v set from storage rlk:io src.stats.electroBonus
execute if data storage rlk:io src.stats.electroBonus run function rlk:items/lore/electrobonus with storage rlk:io
execute if data storage rlk:io src.stats.cryoBonus run data modify storage rlk:io v set from storage rlk:io src.stats.cryoBonus
execute if data storage rlk:io src.stats.cryoBonus run function rlk:items/lore/cryobonus with storage rlk:io
execute if data storage rlk:io src.stats.geoBonus run data modify storage rlk:io v set from storage rlk:io src.stats.geoBonus
execute if data storage rlk:io src.stats.geoBonus run function rlk:items/lore/geobonus with storage rlk:io
execute if data storage rlk:io src.stats.anemoBonus run data modify storage rlk:io v set from storage rlk:io src.stats.anemoBonus
execute if data storage rlk:io src.stats.anemoBonus run function rlk:items/lore/anemobonus with storage rlk:io
execute if data storage rlk:io src.stats.dendroBonus run data modify storage rlk:io v set from storage rlk:io src.stats.dendroBonus
execute if data storage rlk:io src.stats.dendroBonus run function rlk:items/lore/dendrobonus with storage rlk:io

# 2) 특수 능력 (abilities: 여러 줄 그대로 추가)
execute if data storage rlk:io src.abilities[0] run data modify storage rlk:io lore append value {text:"",italic:false}
data modify storage rlk:io aq set from storage rlk:io src.abilities
# 숫자 자리표가 있는 설명은 지금 값으로 바꾼 사본(rlk:items disp.<id>, items/tune/disp_build)
function rlk:items/tune/disp_get with storage rlk:io
execute if data storage rlk:io src.abilities[0] run function rlk:items/ability_loop

# 2.5) 각인 (engravings: 이름을 한 줄로)
execute if data storage rlk:io src.engravings[0] run function rlk:items/lore/engr
# 3) 설명 (desc: 여러 줄 그대로 추가)
execute if data storage rlk:io src.desc[0] run data modify storage rlk:io lore append value {text:"",italic:false}
data modify storage rlk:io dq set from storage rlk:io src.desc
execute if data storage rlk:io src.desc[0] run function rlk:items/desc_loop

# 4) 인벤토리 아이템: 클릭 드롭 안내 (clickdrop 플래그)
execute if data storage rlk:io clickdrop run data modify storage rlk:io lore append value {text:"",italic:false}
execute if data storage rlk:io clickdrop run data modify storage rlk:io lore append value {text:"클릭하면 버립니다",color:"gray",italic:true}
