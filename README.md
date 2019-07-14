# Raspberry-remove
树莓派远程桌面显示更改，
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
如果刚刚安装的是最新系统不用更新固件不用执行sudo rpi-update
在安装软件是可以先更新源，如果出现依赖问题，把源换回官方的吧。
