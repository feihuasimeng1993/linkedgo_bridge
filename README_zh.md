# 零狗智能HomeAssistant插件

[English](./README.md) | [简体中文](.README_zh.md)

<p align="left">
  <img src="https://omo-oss-image.thefastimg.com/portal-saas/pg2024022210453839417/cms/image/314152a9-c7a1-4082-8a0e-d7e5c7f81df9.png_186xaf.png" alt="零狗智能" title="零狗智能" la="la">
</p>

Linekdgo Bridge 是由零狗官网提供支持的 Home Assistant 的集成组件，用于在 Home Assistant 平台控制您的零狗智能设备，目前已经支持温控类产品（ST830 蓝牙青春版, ST1800-HN 单地暖, ST2000 极光板）。

## 安装

> Home Assistant 版本要求：
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0


### 方法: [HACS](https://hacs.xyz/)

一键从 HACS 安装 Linkedgo Bridge 集成：

HACS > 在搜索框中输入 **linkedgo Bridge** > 点击 **linkedgo Bridge** ，进入集成详情页  > DOWNLOAD

## 配置

### 零狗APP
1. 下载零狗APP，并注册用户账号
2. 创建住宅
3. 使用零狗APP完成设备添加，并分配楼层、房间信息

### Linkedgo Bridge 登录

[设置 > 设备与服务 > 添加集成](https://my.home-assistant.io/redirect/brand/?brand=linkedgo) > 搜索“`Linkedgo Bridge`” > 下一步 > 请点击此处进行登录 > 使用零狗APP账号登录

[![打开您的 Home Assistant 实例并开始配置一个新的 Linkedgo Bridge 集成实例。](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=linkedgo bridge)

### 添加零狗设备

登录成功后，会弹出会话框“选择住宅与设备”。您可以选择需要添加的零狗住宅，该住宅内的所有设备将导入 Home Assistant 。
