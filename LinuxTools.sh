#!/bin/bash
version="v3.1"
version_log="Fedora 系统支持"

RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
PLAIN="\033[0m"

red(){
    echo -e "\033[31m\033[01m$1\033[0m"
}

green(){
    echo -e "\033[32m\033[01m$1\033[0m"
}

yellow(){
    echo -e "\033[33m\033[01m$1\033[0m"
}

REGEX=("debian" "ubuntu" "centos|red hat|kernel|oracle linux|alma|rocky" "'amazon linux'" "alpine")
RELEASE=("Debian" "Ubuntu" "CentOS" "CentOS" "Alpine")
PACKAGE_UPDATE=("apt -y update" "apt -y update" "yum -y update" "yum -y update" "apk update -f")
PACKAGE_INSTALL=("apt -y install" "apt -y install" "yum -y install" "yum -y install" "apk add -f")
CMD=("$(grep -i pretty_name /etc/os-release 2>/dev/null | cut -d \" -f2)" "$(hostnamectl 2>/dev/null | grep -i system | cut -d : -f2)" "$(lsb_release -sd 2>/dev/null)" "$(grep -i description /etc/lsb-release 2>/dev/null | cut -d \" -f2)" "$(grep . /etc/redhat-release 2>/dev/null)" "$(grep . /etc/issue 2>/dev/null | cut -d \\ -f1 | sed '/^[ ]*$/d')")

for i in "${CMD[@]}"; do
	SYS="$i" && [[ -n $SYS ]] && break
done

for ((int=0; int<${#REGEX[@]}; int++)); do
	[[ $(echo "$SYS" | tr '[:upper:]' '[:lower:]') =~ ${REGEX[int]} ]] && SYSTEM="${RELEASE[int]}" && [[ -n $SYSTEM ]] && break
done

[[ -z $SYSTEM ]] && red "脚本暂时不支持VPS的当前系统，请使用主流操作系统" && exit 1
[[ ! -f /etc/ssh/sshd_config ]] && sudo ${PACKAGE_UPDATE[int]} && sudo ${PACKAGE_INSTALL[int]} openssh-server
[[ -z $(type -P curl) ]] && sudo ${PACKAGE_UPDATE[int]} && sudo ${PACKAGE_INSTALL[int]} curl




check_status(){
    yellow "正在检查VPS系统状态..."
    if [[ -z $(type -P curl) ]]; then
        yellow "检测curl未安装，正在安装中..."
        if [[ ! $SYSTEM == "CentOS" ]]; then
            ${PACKAGE_UPDATE[int]}
        fi
        ${PACKAGE_INSTALL[int]} curl
    fi
    if [[ -z $(type -P sudo) ]]; then
        yellow "检测sudo未安装，正在安装中..."
        if [[ ! $SYSTEM == "CentOS" ]]; then
            ${PACKAGE_UPDATE[int]}
        fi
        ${PACKAGE_INSTALL[int]} sudo
    fi


}



open_ports(){
    systemctl stop firewalld.service 2>/dev/null
    systemctl disable firewalld.service 2>/dev/null
    setenforce 0 2>/dev/null
    ufw disable 2>/dev/null
    iptables -P INPUT ACCEPT 2>/dev/null
    iptables -P FORWARD ACCEPT 2>/dev/null
    iptables -P OUTPUT ACCEPT 2>/dev/null
    iptables -t nat -F 2>/dev/null
    iptables -t mangle -F 2>/dev/null
    iptables -F 2>/dev/null
    iptables -X 2>/dev/null
    netfilter-persistent save 2>/dev/null
    green "VPS的防火墙端口已放行！"
    echo ""  
    echo -e "${YELLOW}1秒进入主菜单${YELLOW}"
    echo "" 
    sleep 1s 

    menu

}



Root_sh(){

    echo ""    
    
    echo ""

    IP=$(curl -sm8 ip.sb)

    sudo lsattr /etc/passwd /etc/shadow >/dev/null 2>&1
    sudo chattr -i /etc/passwd /etc/shadow >/dev/null 2>&1
    sudo chattr -a /etc/passwd /etc/shadow >/dev/null 2>&1
    sudo lsattr /etc/passwd /etc/shadow >/dev/null 2>&1

    read -p "输入要设置的SSH端口（默认22）：" sshport
    [[ -z $sshport ]] && red "端口未设置，将使用默认22端口" && sshport=22
    read -p "输入设置的root密码：" password
    [[ -z $password ]] && red "密码未设置，将使用随机生成密码" && password=$(cat /proc/sys/kernel/random/uuid)
    echo root:$password | sudo chpasswd root

    sudo sed -i "s/^#\?Port.*/Port $sshport/g" /etc/ssh/sshd_config;
    sudo sed -i "s/^#\?PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config;
    sudo sed -i "s/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config;

    sudo service ssh restart >/dev/null 2>&1 # 某些VPS系统的ssh服务名称为ssh，以防无法重启服务导致无法立刻使用密码登录
    sudo service sshd restart >/dev/null 2>&1

    yellow "VPS root登录信息设置完成！"
    green "VPS登录地址：$IP:$sshport"
    green "用户名：root"
    green "密码：$password"
    yellow "请妥善保存好登录信息！然后重启VPS确保设置已保存！"
}


menu(){

    echo "#############################################################"
    echo -e "#                   ${RED}Misaka Linux Toolbox${PLAIN}                      #"
    echo -e "# ${GREEN}作者${PLAIN}: Misaka 的小姐妹                                     #"
    echo -e "# ${GREEN}网址${PLAIN}: https://owo.misaka.rest                             #"
    echo -e "# ${GREEN}论坛${PLAIN}: https://vpsgo.co                                    #"
    echo -e "# ${GREEN}TG群${PLAIN}: https://t.me/misakanetcn                            #"
    echo -e "# ${GREEN}GitHub${PLAIN}: https://github.com/Misaka-blog                    #"
    echo -e "# ${GREEN}Bitbucket${PLAIN}: https://bitbucket.org/misakano7545             #"
    echo -e "# ${GREEN}GitLab${PLAIN}: https://gitlab.com/misaka-blog                    #"
    echo "#############################################################"
    echo ""
    echo -e " ${GREEN}1.${PLAIN} 开放系统防火墙端口"
    echo -e " ${GREEN}2.${PLAIN} 修改登录方式为 root + 密码"
    # echo -e " ${GREEN}3.${PLAIN} 节点相关"
    # echo -e " ${GREEN}4.${PLAIN} 性能测试"
    # echo -e " ${GREEN}5.${PLAIN} VPS探针"
    echo " -------------"
    echo -e " ${GREEN}9.${PLAIN} 更新脚本"
    echo -e " ${GREEN}0.${PLAIN} 退出脚本"
    echo ""
    echo -e "${YELLOW}当前版本${PLAIN}：$version"
    echo -e "${YELLOW}更新日志${PLAIN}：$version_log"
    echo ""

    read -rp " 请输入选项 [0-9]:" menuInput
    case $menuInput in
        1) open_ports ;;
        2) Root_sh ;;

        # 1) menu1 ;;
        # 2) menu2 ;;
        # 3) menu3 ;;
        # 4) menu4 ;;
        # 5) menu5 ;;
		# 9) wget -N https://raw.githubusercontent.com/misaka-gh/MisakaLinuxToolbox/master/MisakaToolbox.sh && chmod +x MisakaToolbox.sh && bash MisakaToolbox.sh ;;
        *) exit 1 ;;
    esac
}


clear
check_status
menu
