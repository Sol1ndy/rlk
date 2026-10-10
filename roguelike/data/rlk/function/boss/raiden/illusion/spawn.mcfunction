$function rlk:boss/raiden/object/create {kind:2,model:"illusion_ready",hp:1,id:$(id),y:0}
$execute as @e[tag=rlk_rd_object,scores={rdObjKind=2,rdObjId=$(id)},tag=!rlk_rd_illusion,limit=1] run function rlk:boss/raiden/illusion/adopt
