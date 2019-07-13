# Raspberry-remove
树莓派远程桌面显示更改
更改boot下config.txt

![avatar](1.png)
用热点链接：
1.安装完系统后在该目录下新建wpa_supplicant.conf文件填入以下信息:

country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
 
network={
ssid="WiFi-A"
psk="12345678"
key_mgmt=WPA-PSK
priority=1
}


![avatar](2.png)
