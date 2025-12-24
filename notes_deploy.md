# notes_deploy.md

`cd /mnt/d/work/docker_practice_3_multiservice`
進到這次部署練習的專案資料夾（所有 docker/git 指令都在這裡做）。

`docker compose up --build`
用 docker-compose.yml 把「redis + web」整套跑起來；web 會先依 Dockerfile build 成 image，再建立 container 啟動。

`docker compose ps`
看目前 compose 開了哪些 container、各自狀態、以及哪些 ports 有對外映射。

`docker compose logs -f web`
追蹤 web 這個服務的即時 log（你看到 GET /count 200 就是有人成功打到它）。

`curl -i http://localhost:5000/`
從你本機打到 web 的 `/`，確認 web 有回應（200/內容）。

`curl -i http://localhost:5000/count`
從你本機打到 web 的 `/count`，確認 hits 會增加（代表 web 真的連得到 redis）。

`docker compose exec web bash`
直接「進入」正在跑的 web container 裡面開一個 bash（用來檢查容器內環境）。

`python -c "import redis; print('ok')"`
在 web 容器裡跑一個小測試，確認 python 套件（redis）真的裝好了。

`exit`
離開容器回到本機 terminal。

`docker compose down`
把 compose 開的所有 container/網路關掉（整套服務停掉）。

`git status`
看你現在有哪些檔案被改到、哪些還沒加入 staging。

`git add .`
把目前資料夾底下改動全部加入 staging（準備要 commit 的內容）。

`git commit -m "..." `
把 staging 的改動打包成一個 commit（這是本機 repo 的版本紀錄點）。

`git push -u origin master`
把「本機 master 分支」推到「GitHub 上的 origin/master」（遠端 repo 更新）。

`git remote -v`
看 origin 指向哪個 GitHub repo URL（用來確認你到底推到哪個專案）。

（GitHub 網頁）新增 `.github/workflows/ci.yml`
這個檔案是 GitHub Actions 的「流程腳本」；push/PR 觸發後就照它跑 CI/CD。

（GitHub Actions）CI 失敗：`ModuleNotFoundError: No module named 'app'`
代表 pytest 在 CI 環境找不到你的 app.py（import path 問題）。

（修 CI）在 workflow 的 Run tests 加上 `PYTHONPATH`，並改用 `python -m pytest`
讓 CI 的 Python 知道「專案根目錄在哪」，pytest 才 import 得到 `app`。

（Render 網頁）New Key Value（Free）→ 複製 Internal URL
這步是在雲端開一個 Redis，拿到它的連線位址（之後 web 用 REDIS_URL 連它）。

（Render 網頁）New Web Service（Docker）→ 設 `REDIS_URL`
Render 會從 GitHub 抓 repo，用 Dockerfile build，跑成一個對外提供網址的 web 服務。

（Render 網頁）Settings → Auto Deploy：Off
關掉「看到你 push 就自動部署」；改走你要練的 B 流程（CI 過才部署）。

（Render 網頁）Settings → Deploy Hooks：Copy URL
拿到一個「部署按鈕網址」（打它一下 Render 才會開始 deploy）。

（GitHub 網頁）Secrets → Actions：新增 `RENDER_DEPLOY_HOOK`
把 Deploy Hook URL 放進 secret，讓 workflow 可以安全地用，不要寫死在程式碼裡。

（GitHub Actions）deploy job：`curl -X POST "$RENDER_DEPLOY_HOOK"`
CI 綠燈後才會打 Render 的 Deploy Hook → 觸發 Render 部署（這就是 CD）。

`curl -i https://你的-render-網址/`
部署成功後，用 Render 給的公開網址測 `/`，確認線上服務真的活著。

`curl -i https://你的-render-網址/count`
測 `/count`，hits 會增加就代表線上 web ↔ 線上 redis 真的連通。

（收尾）Render 刪掉 Web Service + Key Value
把雲端資源關掉/刪掉，避免留著佔用或產生任何後續疑慮。

（收尾）GitHub 刪掉 Secret：`RENDER_DEPLOY_HOOK`
把部署用的秘密網址從 GitHub 移除，避免以後誤觸或外洩風險。
