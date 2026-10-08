# macro: id = 석판 옆 아이템
data modify storage rlk:scan s set value {atkPct:0,atkFlat:0,hpPct:0,hpFlat:0,defPct:0,defFlat:0,elemMastery:0,critChance:0,critDamage:0,moveSpeed:0,atkSpeed:0,energyRecharge:0,physBonus:0,pyroBonus:0,hydroBonus:0,electroBonus:0,cryoBonus:0,geoBonus:0,anemoBonus:0,dendroBonus:0}
$data modify storage rlk:scan s merge from storage rlk:items registry.$(id).stats
function rlk:items/slate/add with storage rlk:scan s
