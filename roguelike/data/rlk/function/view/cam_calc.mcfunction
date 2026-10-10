# 카메라 오프셋(rlk:view cam) → 한 단계 이동량(st.x/y/z)과 두 단계 앞 검사점(st.lx/ly/lz). 로컬 좌표: ^왼쪽 ^위 ^앞
function rlk:view/burst_camera_scale
execute store result score #bcX view run data get storage rlk:view cam.right -100000
execute store result score #bcY view run data get storage rlk:view cam.up 100000
execute store result score #bcZ view run data get storage rlk:view cam.back -100000
scoreboard players operation #bcX view *= #bcMul view
scoreboard players operation #bcY view *= #bcMul view
scoreboard players operation #bcZ view *= #bcMul view
scoreboard players operation #bcX view /= #100 tmp
scoreboard players operation #bcY view /= #100 tmp
scoreboard players operation #bcZ view /= #100 tmp
# 본체에서 카메라까지의 방향과 기존 14단계 벽 충돌 검사는 유지한다.
execute store result storage rlk:view st.x double 0.0000007143 run scoreboard players get #bcX view
execute store result storage rlk:view st.y double 0.0000007143 run scoreboard players get #bcY view
execute store result storage rlk:view st.z double 0.0000007143 run scoreboard players get #bcZ view
execute store result storage rlk:view st.lx double 0.0000014286 run scoreboard players get #bcX view
execute store result storage rlk:view st.ly double 0.0000014286 run scoreboard players get #bcY view
execute store result storage rlk:view st.lz double 0.0000014286 run scoreboard players get #bcZ view
