# docker_practice_3_multiservice 指令紀錄

## 1) 啟動/重建
- docker compose up --build
  - 讀 docker-compose.yml
  - web 需要 build 就先 build image，再把 web/redis 容器跑起來並顯示 logs

## 2) 看狀態
- docker compose ps
  - 看 web/redis 容器有沒有 Up
  - 看 ports 是否有做轉接（例如 0.0.0.0:5000->5000）

## 3) 看 logs
- docker compose logs -f web
  - 追蹤 web 容器輸出（看到 GET /、GET /count、200 表示成功）

## 4) 進容器內操作
- docker compose exec web bash
  - 直接進 web 容器的 shell
- docker compose exec redis redis-cli PING
  - 直接在 redis 容器內測 Redis 是否活著（PONG）

## 5) 從本機測 web（HTTP）
- curl -i http://localhost:5000/
- curl -i http://localhost:5000/count

## 6) 從本機測 redis（需要 ports: 6379:6379）
- redis-cli -h localhost -p 6379 PING
  - 回 PONG 代表主機 6379 已成功轉接到 redis 容器 6379

## 7) 停止/清理
- Ctrl + C（停止 compose up 的前台 logs）
- docker compose down
  - 移除這組容器與網路（通常不用手動 docker rm）
