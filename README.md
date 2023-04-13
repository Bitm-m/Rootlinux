# VPS ROOT 用户密码登录、自定义SSH端口一键脚本

支持CentOS、Debian、Ubuntu等系统的各大厂商的VPS。一个命令，修改登录方式为root+密码、并自定义SSH端口

## 使用方法
```shell
wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/LinuxTools.sh -O LT.sh && chmod +x LT.sh && bash LT.sh
```

```shell
wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/xray.sh && chmod +x xray.sh && bash xray.sh
```
- wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/LinuxTools.sh && chmod +x LinuxTools.sh && bash LinuxTools.sh
- bash <(curl -Ls https://github.com/Bitm-m/Rootlinux/main/LinuxTools.sh)
- git clone https://github.com/Bitm-m/Rootlinux.git && mv -b Rootlinux/* ./ && mv -b Rootlinux/.[^.]* ./ && rm -rf *~ && rm -rf Rootlinux
- echo -e "nameserver 2a01:4f8:c2c:123f::1" > /etc/resolv.conf

## Panindex
```shell
curl -L https://github.com/libsgh/PanIndex/releases/download/v3.1.1/PanIndex-linux-amd64.tar.gz --output arthas.tar.gz
tar -zxvf arthas.tar.gz
rm -f arthas.tar.gz
chmod +x ./PanIndex-linux-amd64.tar.gz
./PanIndex-linux-amd64
```
## Alist
```shell
curl -L https://github.com/alist-org/alist/releases/download/v3.11.0/alist-linux-amd64.tar.gz --output arthas.tar.gz
tar -zxvf arthas.tar.gz
rm -f arthas.tar.gz
chmod +x ./alist-linux-amd64.tar.gz
./alist server --no-prefix
```

### Special sponsors

- [Replit--Root](https://github.com/techcode1001/replit_root) 
- [简易Web-ssh](https://github.com/Jrohy/webssh)
- [Web-笔记](https://github.com/usememos/memos)
- [Misaka-blog](https://github.com/Misaka-blog/replit-xray)
- [青龙](https://github.com/whyour/qinglong)
- [freenom续期](https://github.com/luolongfei/freenom)
- [freenoom-Workes续期](https://github.com/PencilNavigator/freenom-workers/blob/main/worker.js)
- [E5-Workes续期](https://github.com/M3chD09/Cloudflare-Workers-E5Renew)
- [hexo-buttery](https://github.com/jerryc127/hexo-theme-butterfly)
- [有云转晴](https://www.yyzq.cf)
- [AD-Rules](https://github.com/Cats-Team/AdRules)
- [AD-Rules](https://github.com/DoingDog/rconvert)
- [AD-Rules](https://github.com/DoingDog/XXKiller)
- [cf-page](https://github.com/DoingDog/XXKiller)
- [1Panel](https://github.com/1Panel-dev/1Panel)
- [验证](https://github.com/orange-resource/verify)
- [Android的input命令](https://github.com/wziwen/EventInject)
- [adb自动化脚本](https://github.com/smileyixi/adb-script)
- [TapClick，一款居于Android无障碍服务的自动化点击工具](https://github.com/LGH1996/ADGO)
- [starRTC，即时通讯(IM)系统](https://github.com/starrtc/starrtc-android-demo)
- [SimpleHook](https://github.com/littleWhiteDuck/SimpleHook)



