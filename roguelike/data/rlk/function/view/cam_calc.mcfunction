# 카메라 오프셋(rlk:view cam) → 한 단계 이동량(st.x/y/z)과 두 단계 앞 검사점(st.lx/ly/lz). 로컬 좌표: ^왼쪽 ^위 ^앞
execute store result storage rlk:view st.x double 0.0000007143 run data get storage rlk:view cam.right -100000
execute store result storage rlk:view st.y double 0.0000007143 run data get storage rlk:view cam.up 100000
execute store result storage rlk:view st.z double 0.0000007143 run data get storage rlk:view cam.back -100000
execute store result storage rlk:view st.lx double 0.0000014286 run data get storage rlk:view cam.right -100000
execute store result storage rlk:view st.ly double 0.0000014286 run data get storage rlk:view cam.up 100000
execute store result storage rlk:view st.lz double 0.0000014286 run data get storage rlk:view cam.back -100000
