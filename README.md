# basic-chatbot

Pas testing Snyk Readteam Feature

https://docs.snyk.io/developer-tools/snyk-cli/commands/redteam#configuration-file

## Setup

```
$ Git clone https://github.com/papicella/basic-chatbot
$ cd basic-chatbot
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
```

## Run

```
╰─$ python main.py
🤖 Loading Model: distilgpt2...
✅ Model loaded successfully.
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
🤖 Loading Model: distilgpt2...
✅ Model loaded successfully.
 * Debugger is active!
 * Debugger PIN: 841-512-339
```

## Test

```
╰─$ curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"prompt": "What is the capital of France?"}'
{
  "message": "\u201d\n\nThe French government has come under fire for its attempt to use a country\u2019s currency to cover the cost of living and to create an alternative currency.\nFrance is an EU member and, as of now, France is a member. France has been in the Eurozone since 1949. The euro is currently pegged at about \u20ac15.1 billion. But there has also been anger at what some say is inadequate support for the new currency in"
}
```

## Readteam the chatbot API using Snyk CLI

```
$ snyk redteam --experimental
```
