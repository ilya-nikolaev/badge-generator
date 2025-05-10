# Badge generator

A simple badge generator for displaying stats — built with **FastAPI**, uses **Redis** for caching.


## Examples

![LeetCode badge](https://badges.rnurnu.ru/leetcode/40/ilya-nikolaev)


## Run

> Note: The default MTU is set to 1450. If you need a different value, you can change it in docker-compose.yml under the networks section.

```bash
git clone https://github.com/ilya-nikolaev/badge-generator
cd badge-generator
cp .config/config.example.toml .config/config.toml
nano .config/config.toml  # Replace 'nano' with your preferred editor
docker compose up --build
```

The service will run on port `9080`.

Documentation will be available at: http://localhost:9080/docs

## Nginx

If you want to set up Nginx, use the `badge-generator.nginx` file.
It includes configuration for SSL, headers, and gzip.
To generate SSL certificates, you can use [Certbot](https://certbot.eff.org/).
