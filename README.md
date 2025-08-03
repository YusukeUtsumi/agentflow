# AgentFlow v0.3
YAML1枚でLLMやスクリプトを連携させて働かせるためのフレームワーク

## 更新内容
・並行処理化  
・sample.yamlテンプレの更新  
・ステップ用テンプレの追加  

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
```bash
agentflow/  
├─ agentflow_runner.py       # 実行エントリーポイント  
├─ templates/                # ステップ用のテンプレ  
│      ├─ market/
│      │     ├─ market_idea.py  
│      │     ├─ market_research.py
│      │     ├─ report.py
│      │     └─ sample.yaml  
│      └─ search-output/
│            ├─ market_research.py  
│            ├─ output.py  
│            └─ sample.yaml  
└─ README.md  
```

## 使い方
### YAMLを定義
```yaml:templates/sample.yaml
steps:
  - id: agent_a
    handler: python
    module: templates.market.market_research
    input: ""
    parallel: true

  - id: agent_b
    handler: python
    module: templates.market.market_idea
    input: "{{agent_a.output}}"
    parallel: true

  - id: agent_c
    handler: python
    module: templates.market.report
    input: "{{agent_a.output}} + {{agent_b.output}}"
    parallel: false
```

### 実行
```bash
python agentflow_runner.py templates/market/sample.yaml
```
## ライセンス
MIT License
