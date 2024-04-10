# ARSAGA_STABLE_DIFFUSION
chatGPT + Stable Diffusionを使用した画像生成用のpythonモジュール

## 動作環境
- Python: ^3.11
- langchain: ^0.1.12
- openai = "^1.14.0"

ライブラリの詳細はpyproject.tomlを確認してください。
LLM周りはアップデートが激しいので依存関係に注意してください。

# インストール
このリポジトリのurlを指定してpip, poetry等でインストールしてください。
インストール例
```text
[tool.poetry.dependencies]
arsaga-stable-diffusion = {git = "https://github.com/...url...", branch = "お好きなブランチ"}
```

## 構成
```text
.
├── README.md
├── arsaga_stable_diffusion // ライブラリの本体
│   ├── __init__.py
│   ├── errors // ライブラリで発生するエラーを定義したディレクトリ
│   │   ├── __init__.py
│   │   ├── error_message.py
│   │   └── exceptions.py
│   ├── openai // LLMを使用するクラスを定義したディレクトリ
│   │   ├── __init__.py
│   │   └── prompt_generator.py
│   ├── prompt // ライブラリ内で使用するプロンプトのテンプレート
│   │   ├── __init__.py
│   │   └── template.py
│   ├── schemas // 変数や返値の定義したディレクトリ
│   │   ├── __init__.py
│   │   ├── image.py
│   │   └── types.py
│   └── stable_diffusion // Stable Diffusionを使用するクラスを定義したディレクトリ
│       ├── __init__.py
│       ├── base.py
│       └── image_generator.py
├── makefile
├── poetry.lock
├── pyproject.toml
├── pyrightconfig.json // pyrightの設定ファイル
└── tests // テストコードのディレクトリ
    ...省略
```

## 使用方法
基本的にプロンプト(自然言語)を受け取り、画像のバイナリ(bytesクラス)を返すことを想定しています。
LLMを使用したクラスがプロンプトを受け取り、文字列(str | Coroutine[str])を返します。
画像生成を行うクラスが何かしらの入力を受け取って画像バイナリを返します。
それぞれのクラスは別々に使用することも可能です。

```python
from arsaga_stable_diffusion.openai import PromptGenerator
from arsaga_stable_diffusion.schemas.types import gpt_type, image_aspect # ←引数の型定義

# LLMのクラスインスタンスを作成
generator = PromptGenerator(model=models, temperature=temperature, verbose=True)

# 画像生成用のクラスインスタンスをメンバ変数へ登録
generator.bind_image_generator()

# メソッドを実行して画像を生成する
image = generator.make_image_by_prompt(prompt=prompt, aspect_ratio=aspect_ratio)

# デコードして 画像表示 or 保存等
decoded_image = image.decode_b64_bytes()

# 画像ファイルを表示するサンプル このライブラリではそこまでの機能は実装しません
io_image = Image.open(decoded_image)
image_np = np.array(io_image)
```

##プロジェクト運用ルール(仮)
- tool.poetryのバージョンについて
    初期ver => 1.0.0 (※ A.B.C とする) ブランチ名: 1.x.x
    破壊的な変更: リポジトリをフォーク(ブランチ変更) A変更, B,Cリセット => 2.0.0 ブランチ名: 2.x.x
    機能追加: Bの変更, Cリセット => 1.1.0
    軽微な修正等: C変更 => 1.0.1

    issueを立てて、作業ブランチ名はバージョン番号を入れるといいかもしれません。