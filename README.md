# fastapi-auth-server

## Run

* Run On Docker

~~~bash

cd fastapi-auth-server

docker-compose up -d --build

~~~


## Set up

### WebAPI

* create `.env` at `/webapi` from `.env.sample`

* create `.venv` at `/webapi` and install library

    ~~~bash
    # 1. 仮想環境の作成
    python -m venv .venv

    # 2. 仮想環境の有効化
    # for Mac
    source .venv/bin/activate

    # for Windows
    .venv/Scripts/activate

    # 3. ライブラリのインストール
    pip install -r requirements.txt
    ~~~