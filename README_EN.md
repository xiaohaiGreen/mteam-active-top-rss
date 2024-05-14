# MTeam Weekly Freeleech Auto-downloader
[切换到中文](README.md)

Automatically download MTeam's weekly large freeleech packs by adding the generated RSS link to your BitTorrent client.

[![Docker Pulls](https://img.shields.io/docker/pulls/xiaohaigreen/mteam-active-top-rss)](https://hub.docker.com/r/xiaohaigreen/mteam-active-top-rss)

## Introduction

This project provides a simple solution for automatically downloading MTeam's weekly large freeleech packs. It generates an RSS link that you can add to your BitTorrent client to enable automatic downloading of corresponding torrent packs.

## Features

- Automatically fetches the latest weekly releases from MTeam.
- Generates an RSS link that you can add to your BitTorrent client for automatic downloading.
- Provides a Docker image for easy deployment.

## Usage

### Docker Deployment

You can deploy this solution using Docker. Follow these steps:

1. Go to the MTeam website and click on "Console" -> "Laboratory" -> "Create access token (X-API-KEY)".

2. Pull the Docker image from Docker Hub:

```bash
docker pull xiaohaigreen/mteam-active-top-rss
```

3. Service deployment:

- Using docker-cli:

```shell
docker run -d -p 5000:5000 -e X-API-KEY=xxx xiaohaigreen/mteam-active-top-rss
```

- Using docker-compose:

```yaml
version: "3.x"
services:
  mteam-active-top-rss:
    image: xiaohaigreen/mteam-active-top-rss:1.0
    container_name: mteam-active-top-rss
    restart: always # Automatically restart the container when the Docker service restarts
    environment:
      - X-API-KEY=xxx
    ports:
      - 5000:5000
```

### Parameters

Optional parameters:

| Parameter          | Values                                          | Explanation                                   | Supported Version |
| ------------------ | ----------------------------------------------- | --------------------------------------------- | ---------------- |
| sort_field         | size,date                                       | Sort by time or size                          | 1.0+             |
| sort_order         | asc,desc                                        | Ascending or descending                       | 1.0+             |
| single_small_than  | integer                                         | Single torrent file smaller than GB value     | 1.0+             |
| single_bigger_than | integer                                         | Single torrent file larger than GB value      | 1.0+             |
| total_small_than   | integer                                         | Total torrent files smaller than GB value     | 1.0+             |
| mode               | "normal","adult","movie","music","tvshow","all" | One or multiple values, or "all"              | 1.0+             |
| free_left          | integer                                         | Remaining freeleech time, in hours            | 1.1+             |

> Examples:
>
> http://127.0.0.1:5000/rss?sort_field=size&sort_order=desc&mode=all
>
> http://127.0.0.1:5000/rss?sort_field=size&sort_order=desc&mode=all&total_small_than=746

### Configuration

After deploying the Docker container, you need to configure your BitTorrent client to use the generated RSS link. Here's how:

1. Access the web interface of the Docker container (usually located at `http://localhost:8080`).
2. Follow the instructions to generate the RSS link.
3. Add the generated RSS link to your BitTorrent client.

## Support

If you have any questions or concerns, please raise an issue on [GitHub](https://github.com/xiaohaiGreen/mteam-active-top-rss/issues).

If this repository has been helpful to you, please give it a star⭐️!
