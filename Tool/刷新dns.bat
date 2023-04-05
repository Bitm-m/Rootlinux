@echo off
chcp 65001
REM 判断当前用户是否为管理员
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 当前用户拥有管理员权限，可以运行脚本。
) else (
    echo 当前用户没有管理员权限，建议以管理员身份运行脚本。
    pause
    goto:eof
)
echo 正在释放并更新 IP 地址...
@ipconfig /release > NUL
@ipconfig /renew > NUL
echo IP 地址已成功释放和更新。
echo.
echo 正在清除 DNS 缓存...
@ipconfig /flushdns > NUL
echo DNS 缓存已成功清除。
echo.
echo 正在重置 TCP/IP 和 IPv4 协议...
@netsh winsock reset > NUL
@netsh int ip reset > NUL
echo TCP/IP 和 IPv4 协议已成功重置。
echo.
echo 网络故障排除完成。
pause
