# eventpix

No Calendar No Life

# 使い方 (現状)

## パッケージ管理ツールのインストール
* [Rye](./backend/CONTRIBUTING.md)
* Node.js

## 実行前準備

```
cd backend
rye sync --no-lock
cd ../frontend
npm install
```

## 実行
それぞれ別のターミナルで実行
```
cd backend
rye run eventpix
```
```
cd fontend
next dev
```

## 確認
(http://localhost:3000)にアクセス
![サンプル](./sample.png)
