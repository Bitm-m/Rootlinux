# VPS ROOT 用户密码登录、自定义SSH端口一键脚本

支持CentOS、Debian、Ubuntu等系统的各大厂商的VPS。一个命令，修改登录方式为root+密码、并自定义SSH端口


## 使用方法
```shell
wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/LinuxTools.sh -O LT.sh && chmod +x LT.sh && bash LT.sh
```

```shell
wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/xray.sh && chmod +x xray.sh && bash xray.sh
```

```shell
wget -N https://raw.githubusercontent.com/Bitm-m/Rootlinux/main/LinuxTools.sh && chmod +x LinuxTools.sh && bash LinuxTools.sh

bash <(curl -Ls https://github.com/Bitm-m/Rootlinux/main/LinuxTools.sh)

git clone https://github.com/Bitm-m/Rootlinux.git && mv -b Rootlinux/* ./ && mv -b Rootlinux/.[^.]* ./ && rm -rf *~ && rm -rf Rootlinux
```

```shell
 echo -e "nameserver 2a01:4f8:c2c:123f::1" > /etc/resolv.conf
```

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
./alist-linux-amd64
```



### Special sponsors

- [找资源 - 阿里云盘资源搜索引擎](https://zhaoziyuan.la/)
- [KinhDown 百度云盘不限速下载！永久免费！已稳定运行3年！非常可靠！Q群 -> 786799372](https://kinhdown.com)
- [JetBrains: Essential tools for software developers and teams](https://www.jetbrains.com/)



