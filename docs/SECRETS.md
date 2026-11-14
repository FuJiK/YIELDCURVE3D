# シークレット管理

このリポジトリには **API キーやサービスアカウント JSON をコミットしません**。

## ローカル開発

1. リポジトリルートで `.env.example` を `.env` にコピーする
2. [Nasdaq Data Link](https://data.nasdaq.com/) と [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) でキーを発行し、`.env` に記入する
3. シェルで読み込むか、IDE の環境変数に設定する

```bash
set -a && source .env && set +a
python yield_curve_3d_us.py
```

各サブディレクトリの `credential/api_key.py` は `QUANDL_API_KEY` / `FRED_API_KEY` を **環境変数から読むだけ** です（値は書かない）。

### Google スプレッドシート（`yieldcurvedata/`）

- サービスアカウント JSON は任意のパスに置き、`GSPREAD_SERVICE_ACCOUNT_JSON` で指定する
- スプレッドシート ID は `GOOGLE_SPREADSHEET_KEY`

## GitHub Actions

ワークフロー [`.github/workflows/update-yield-curve.yml`](../.github/workflows/update-yield-curve.yml) は次のリポジトリシークレットを使います。

| シークレット名 | 用途 |
|---------------|------|
| `QUANDL_API_KEY` | `yield_curve_3d_us.py` のデータ取得 |

**Settings → Secrets and variables → Actions** で登録してください。

## 本番デプロイ（カスタムドメイン）

本番は **gh-pages ブランチ** → `dashboard.theshibsters.com` です。ワークフローが `dist/` を `peaceiris/actions-gh-pages` で公開します（`main` ブランチでの実行時のみ）。

| 出力 | 用途 |
|------|------|
| `dist/index.html` | カスタムドメインルート |
| `dist/yield_curve_3d_us.html` | 従来 URL の互換 |
| `docs/index.html` | main 上のアーカイブ・プレビュー |

`MY_PERSONAL_ACCESS_TOKEN` / `ACTIONS_DEPLOY_KEY` は **不要** です（`GITHUB_TOKEN` で gh-pages 公開と main への HTML コミット）。

## 過去にコミットされていたキーについて

履歴上に平文キーが残っている場合は、**プロバイダ側でキーをローテーション（無効化・再発行）** してください。必要なら [git filter-repo](https://github.com/newren/git-filter-repo) 等で履歴からも除去します。