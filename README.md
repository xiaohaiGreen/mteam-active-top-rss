# MTeam每周免费大包自动下载器
[Switch to English](README_EN.md)

通过在 BitTorrent 客户端中添加生成的 RSS 链接，自动下载 MTeam 每周大包。

[![Docker Pulls](https://img.shields.io/docker/pulls/xiaohaigreen/mteam-active-top-rss)](https://hub.docker.com/r/xiaohaigreen/mteam-active-top-rss)

## 简介

本项目提供了一个简单的解决方案，用于自动下载 MTeam 每周免费大包。它生成一个 RSS 链接，您可以将其添加到 BitTorrent 客户端中，以实现对应种子大包的自动下载。

## 功能特点

- 自动获取 MTeam 的最新每周发布。
- 生成一个 RSS 链接，您可以将其添加到 BitTorrent 客户端，实现自动下载。
- 提供 Docker 镜像，方便部署。

## 使用方法

###  Docker 部署

您可以使用 Docker 部署此解决方案。按照以下步骤操作：

1. 在mteam站点击控制台 -> 实验室 -> 建立存取令牌(X-API-KEY)

2. 从 Docker Hub 上拉取 Docker 镜像：

```bash
docker pull xiaohaigreen/mteam-active-top-rss
```

3.  服务部署：

- 使用 docker-cli：

```shell
docker run -d -p 5000:5000 -e X-API-KEY=xxx xiaohaigreen/mteam-active-top-rss
```

- 使用 docker-compose：

```yaml
version: "3.x"
services:
  mteam-active-top-rss:
    image: xiaohaigreen/mteam-active-top-rss:1.0
    container_name: mteam-active-top-rss
    restart: always # 在Dockers服务重启时，自动重启该容器
    environment:
      - X-API-KEY=xxx
    ports:
      - 5000:5000
```

### 参数

可选参数：

| 参数               | 取值                                            | 解释                      | 支持版本 |
| ------------------ | ----------------------------------------------- | ------------------------- | -------- |
| sort_field         | size,date                                       | 根据时间或者大小排序      | 1.0+     |
| sort_order         | asc,desc                                        | 正序或者倒序              | 1.0+     |
| single_small_than  | 整数                                            | 单个种子文件小于GB值      | 1.0+     |
| single_bigger_than | 整数                                            | 单个种子文件大于GB值      | 1.0+     |
| total_small_than   | 整数                                            | 多个种子文件小于GB值      | 1.0+     |
| mode               | "normal","adult","movie","music","tvshow","all" | 一个或者多个取值，或者all | 1.0+     |
| free_left          | 整数                                            | 剩余free时长，小时        | 1.1+     |

> 样例：
>
> http://127.0.0.1:5000/rss?sort_field=size&sort_order=desc&mode=all
>
> http://127.0.0.1:5000/rss?sort_field=size&sort_order=desc&mode=all&total_small_than=746

### 配置

在部署 Docker 容器之后，您需要配置您的 BitTorrent 客户端以使用生成的 RSS 链接。具体操作如下：

1. 访问 Docker 容器的 Web 界面（通常位于 `http://localhost:8080`）。
2. 按照说明生成 RSS 链接。
3. 将生成的 RSS 链接添加到您的 BitTorrent 客户端。

## 支持

如有任何问题或疑问，请在 [GitHub](https://github.com/xiaohaiGreen/mteam-active-top-rss/issues) 上提出问题。