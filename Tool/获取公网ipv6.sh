ipv4=$(curl -s4m8 ip.p3terx.com -k | sed -n 1p)
ipv6=$(curl -s6m8 ip.p3terx.com -k | sed -n 1p)
filename="output.txt"

# 检查文件是否已存在
if [[ ! -f "$filename" ]]; then
    # 文件不存在，使用 touch 命令创建文件
    touch "$filename"
fi

# 使用 stat 命令获取文件的修改时间
modified_timestamp=$(stat -c "%Y" "$filename")
# 将时间戳转换为精确到分钟的格式
# modified_time=$(date -d "@$modified_timestamp" +"%Y-%m-%d %H:%M")

# 获取当前时间戳
current_timestamp=$(date +%s)
time_diff=$((current_timestamp - modified_timestamp))
current_time=$(date +"%Y-%m-%d %H:%M:%S")

# 转换时间差为格式化字符串
days=$((time_diff / (60 * 60 * 24)))
hours=$((time_diff / (60 * 60) % 24))
minutes=$((time_diff / 60 % 60))
seconds=$((time_diff % 60))
formatted_time=$(printf "%d天 %02d:%02d:%02d" $days $hours $minutes $seconds)

# 使用 grep 过滤空行，并计算非空行的数量
non_empty_line_count=$(grep -v -e '^$' "$filename" | wc -l)

# 将非空行数加1
non_empty_line_count=$((non_empty_line_count + 1))


# 使用grep命令搜索文件中的内容
if grep -q "$ipv6" "$filename"; then
    echo "$non_empty_line_count与上次相隔$formatted_time ip未变化" >> "$filename"
else
    echo "$non_empty_line_count与上次相隔$formatted_time ip发生了变化" >> "$filename"
    echo "$current_time  $ipv6  $ipv4" >> "$filename"
    
fi
