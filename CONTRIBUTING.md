# Eventpix（バックエンド）へのコントリビューション

## 開発環境の構築

1. [Rye](https://rye-up.com/guide/installation/)をインストール

2. 作業用の仮装環境を作成

```bash
rye sync --no-lock
```

3. 正常に動作するか確認

```bash
rye run eventpix
```

## コードの変更

### パッケージの追加

```bash
rye add パッケージ名
```

開発用パッケージ（Ruff や mypy のように直接実行に関わらないパッケージ）を追加する場合は，`--dev`オプションを付与する．

```bash
rye add --dev パッケージ名
```

### パッケージの削除

```bash
rye remove パッケージ名
```

### 環境変数の設定

`backend/.env`を作成し、環境変数を設定する．

```env
API_KEY=xxxxxxxx
```

> [!IMPORTANT]
> API キーなどの重要な情報は必ずソースコード中ではなく.env ファイルに記述すること．またコミット時には，差分に.env ファイルに記述した内容が含まれていないか確認すること．（特にファイル名の打ち間違いに注意する）

## Linter と Formatter の実行

Linter と Formatter には以下のような役割がある．

- Linter: 文法やコーディングスタイルが適切かどうかをチェックする
- Formatter: コードのフォーマットを統一する

当プロジェクトでは Linter と Formatter に[Ruff](https://docs.astral.sh/ruff/)を，また型チェックに[mypy](https://mypy.readthedocs.io/en/stable/)を採用している．コミットは必ずすべてのチェックを通過していることを確認してから行う．

### VSCode を使用する場合

1. VSCode の拡張機能[Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)と[mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)をインストール
2. `.vscode/settings.json`に以下の設定を追加

```json
{
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

3. コード保存時に自動で Linter と Formatter が実行される

### VSCode を使用しない場合

Linter の実行:

```bash
$ rye run ruff check && rye run mypy .
```

Formatter の実行:

```bash
$ rye run ruff check --select I --fix && rye run ruff format
```

> [!NOTE]
> Linter でチェックはされないが，メソッドは 20 行以内で実装することを推奨する．20 行を超えている場合は単一の機能となっていない可能性が高いため，メソッドを分割するなどしてリファクタリングを行う．

## main ブランチへのマージ

main ブランチへのマージは，以下の手順で行う．

1. 作業用ブランチから main ブランチにマージするためのプルリクエストを作成する
2. GitHub Actions のテストを通過し，メンテナ（自分以外）による動作確認が完了したらマージする

> [!TIP] > [act](https://nektosact.com/)を使用すると，ローカルで GitHub Actions のテストを実行できる．ローカルで GitHub Actions の動作を確認する場合はこのツールを使用すると良い．
