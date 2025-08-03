# AgentFlow v0.1
YAML1枚でLLMやスクリプトを連携させて働かせるためのフレームワーク

## 概要
AgentFlowはLLM・スクリプトなどをYAML1枚で定義し、順次実行できる軽量オーケストレーションフレームワークです。
・対話型エージェントではなく、「明示的な道具としてのAI」を実行フローに組み込み
・外部ライブラリやLLMも自由に統合可能
・軽量でRPA的にも使える
LLMに「喋らせる」のではなく、働かせるための構造。

## 特徴
・YAML駆動：複数のエージェントやスクリプトをYAMLで宣言
・シンプルな実行モデル：agentflow_runner.pyのワンコマンド実行
・ステップ間のデータ連携：{{step_id.ファイル名}}プレースホルダーで前のステップの結果を参照可能

## ディレクトリ構成
agentflow/
├─ agentflow_runner.py      # 実行エントリーポイント
├─ templates/               # ステップ用のテンプレ
│   ├─ HelloWorld.js
│   ├─ agent_a.py
│   ├─ agent_b.py
│   └─ sample.yaml
├─ examples/
│   └─ echo.py
└─ README.md

## 使い方
### YAMLを定義
```yaml:templates/sample.yaml
steps:
  - id: agent_a
    handler: python
    module: templates.agent_a
    input: ""

  - id: agent_b
    handler: python
    module: templates.agent_b
    input: "{{agent_a.output}}"
```

### 実行
```bash
python agentflow_runner.py examples/sample.yaml
```
## ライセンス
MIT License
